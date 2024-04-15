import os
import json
import threading
from datetime import datetime
from Nazare_django import settings
from django.views.generic import TemplateView
from index.models.apartments import Apartment
from django.http import JsonResponse, Http404, RawPostDataException
from utils.is_valid_phone import is_valid_phone
from utils.is_valid_captcha import is_valid_captcha
from utils.booking import get_booking_in_range_date
from django.core.exceptions import PermissionDenied
from utils.guest_count import check_guest_count_limit
from utils.json_responses import error_response
from .forms.booking_form import BookingForm, GuestsForm
from booking.models.booking import PAYMENT_METHOD_CHOICES
from utils.send_mail import send_mail_for_client, send_mail_for_admin
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES, MAILING_SUBJECTS


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        context["online_payment"] = settings.ONLINE_PAYMENT

        apartment_id = self.request.GET.get('apartment')
        check_in_date = self.request.GET.get('check_in_date')
        check_out_date = self.request.GET.get('check_out_date')

        adult_count, children_count = 1, 0

        try:
            adult_count = int(self.request.GET.get('adult_count'))
            children_count = int(self.request.GET.get('children_count'))
        except (ValueError, TypeError):
            pass

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

        if check_guest_count_limit(adult_count + children_count, apartment.guest_count):
            context['adult_count'] = adult_count
            context['children_count'] = children_count

        context['apartments'] = Apartment.objects.all()
        return context

    def post(self, request):
        try:
            try:
                data = json.loads(request.body)
            except RawPostDataException:
                return error_response(ERROR_MESSAGES['bad_request'])

            client_data = data.get('clientData')

            for client_key, client_value in client_data.items():
                if client_key == 'payment_method':
                    if client_value == PAYMENT_METHOD_CHOICES[0][0] and not settings.ONLINE_PAYMENT:
                        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_payment_method']}, status=500)
                if client_key == 'client_phone' and not is_valid_phone(client_value):
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_phone']}, status=500)
                if client_key == 'captcha' and not is_valid_captcha(client_value):
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_captcha']}, status=500)
                if client_key == 'guests_count' and int(client_value) <= 0:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)
                if client_key == 'children_count' and int(client_value) < 0:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)
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
                guest_form = GuestsForm(guest_form_data)
                if guest_form.is_valid():
                    guest_instance = guest_form.save(commit=False)
                    guest_instance.booking = booking_instance
                    guest_instance.save()
                else:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)
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
        if booking_dict:
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
