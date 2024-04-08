import os
import threading
from django.views.generic import TemplateView
from Nazare_django import settings
from booking.models.booking import Booking, PAYMENT_METHOD_CHOICES
from index.models.apartments import Apartment
from utils.booking import get_booking_in_range_date
from utils.is_valid_phone import is_valid_phone
from .forms.booking_form import BookingForm, Guest
from utils.send_mail import send_mail_for_client, send_mail_for_admin
import json
from django.http import JsonResponse, Http404
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES, MAILING_SUBJECTS
from datetime import datetime
from django.core.exceptions import PermissionDenied


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        context["online_payment"] = settings.ONLINE_PAYMENT

        apartment_id = self.request.GET.get('apartment')
        check_in_date = self.request.GET.get('check_in_date')
        check_out_date = self.request.GET.get('check_out_date')
        adult_count = self.request.GET.get('adult_count')
        children_count = self.request.GET.get('children_count')

        if apartment_id:
            try:
                try:
                    apartment = Apartment.objects.get(id=apartment_id)
                except ValueError:
                    raise Http404
                context['default_apartment'] = apartment
                context['guest_max'] = apartment.guest_count
            except Apartment.DoesNotExist:
                apartment = Apartment.objects.first()
                context['default_apartment'] = apartment
                context['guest_max'] = apartment.guest_count
        else:
            apartment = Apartment.objects.first()
            context['default_apartment'] = apartment
            try:
                context['guest_max'] = apartment.guest_count
            except AttributeError:
                raise PermissionDenied()

        if check_in_date and check_out_date:
            context['check_in_date'] = check_in_date
            context['check_out_date'] = check_out_date

        if adult_count and children_count:
            context['adult_count'] = adult_count
            context['children_count'] = children_count

        apartment_dict = Apartment.objects.all()
        context['apartments'] = apartment_dict

        booking_list = {}
        for apartment in apartment_dict:
            booking_list[apartment.id] = []
            for booking in Booking.objects.filter(apartment=apartment.id):
                if booking.check_out_date >= datetime.today().date() and booking.confirmed:
                    booking_list[apartment.id].append([
                        booking.check_in_date.strftime("%Y-%m-%d"),
                        booking.check_out_date.strftime("%Y-%m-%d")
                    ])
        context['booking_list'] = booking_list
        return context

    def post(self, request):
        try:
            data = json.loads(request.body)
            client_data = data.get('clientData', {})

            for client_key, client_value in client_data.items():
                if client_key == 'payment_method':
                    if client_value == PAYMENT_METHOD_CHOICES[0][0] and settings.ONLINE_PAYMENT is False:
                        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_payment_method']}, status=500)
                if client_key == 'client_phone' and is_valid_phone(client_value) is False:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_phone']}, status=500)
                if client_key == 'captcha' and len(client_value) == 0:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_captcha']}, status=500)
            guest_data = data.get('guestData', [])
            for guest in guest_data:
                if not type(guest) is dict:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save(commit=False)

            if not self.check_available_date(client_data):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['unavailable_period']}, status=500)

            if not self.check_guest_count(guest_data, booking_instance):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

            if not self.check_price(client_data):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

            if not self.check_privacy_policy(client_data):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_privacy_policy']}, status=500)

            booking_instance.save()

            self.send_mailing(booking_instance)

            for guest_form_data in guest_data:
                Guest.objects.create(
                    guest_second_name=guest_form_data['guest_surname'],
                    guest_name=guest_form_data['guest_name'],
                    guest_father_name=guest_form_data['guest_father_name'],
                    citizenship=guest_form_data['citizenship'],
                    booking=booking_instance,
                )
            return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_booking']}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

    def send_mailing(self, booking_instance):
        base_context = {
            'booking_id': booking_instance.id,
            'apartment': Apartment.objects.get(id=booking_instance.apartment.id).title,
            'name': booking_instance.client_name,
            'check_in': booking_instance.check_in_date,
            'check_out': booking_instance.check_out_date,
            'total_sum': booking_instance.total_sum,
        }

        admin_context = {
            **base_context,
            'phone': booking_instance.client_phone,
            'created': booking_instance.created_at,
            'payment_method': booking_instance.get_payment_method_display(),
        }

        client_context = {
            **base_context,
            'check_in_time': os.getenv('CHECK_IN_TIME'),
            'check_out_time': os.getenv('CHECK_OUT_TIME'),
        }

        threading.Thread(target=send_mail_for_admin,
                         args=(MAILING_SUBJECTS['booking_admin'], 'mailing/admin_booking.html', admin_context)).start()

        if booking_instance.payment_method == PAYMENT_METHOD_CHOICES[1][0]:
            threading.Thread(target=send_mail_for_client,
                             args=(MAILING_SUBJECTS['booking_client'], booking_instance.client_mail,
                                   'mailing/client_booking_offline.html', client_context)).start()
        elif booking_instance.payment_method == PAYMENT_METHOD_CHOICES[0][0]:
            threading.Thread(target=send_mail_for_client,
                             args=(MAILING_SUBJECTS['booking_client'], booking_instance.client_mail,
                                   'mailing/client_booking_online.html', client_context)).start()

    def check_available_date(self, client_data):
        try:
            check_in_date = client_data['check_in_date']
            check_out_date = client_data['check_out_date']
            apartment = client_data['apartment']
        except ValueError:
            return False

        booking_dict = get_booking_in_range_date(check_in_date, check_out_date)
        if booking_dict is not False:
            for booking in booking_dict:
                if booking.confirmed and int(apartment) == booking.apartment.id:
                    return False
        else:
            return False
        return True

    def check_price(self, client_data):
        try:
            check_in_date = datetime.strptime(client_data['check_in_date'], "%Y-%m-%d")
            check_out_date = datetime.strptime(client_data['check_out_date'], "%Y-%m-%d")
            days = (check_out_date - check_in_date).days
            daily_price = Apartment.objects.get(id=int(client_data["apartment"])).daily_price * days
        except ValueError:
            return False

        if int(client_data['total_sum']) != daily_price:
            return False
        return True

    def check_guest_count(self, guest_data, booking_instance):
        if 0 < len(guest_data) <= Apartment.objects.get(id=booking_instance.apartment.id).guest_count:
            if len(guest_data) != booking_instance.guests_count:
                return False
        else:
            return False
        return True

    def check_privacy_policy(self, client_data):
        if not client_data["is_privacy_policy"]:
            return False
        return True
