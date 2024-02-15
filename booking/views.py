import threading
from django.views.generic import TemplateView
from booking.models.booking import *
from index.models.apartments import *
from utils.booking import get_booking_in_range_date
from .forms.booking_form import *
from utils.send_mail import *
import json
from django.http import JsonResponse
from utils.constants import *
from datetime import datetime


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
                apartment = Apartment.objects.get(id=apartment_id)
                context['default_apartment'] = apartment
                context['guest_max'] = apartment.guest_count
            except Apartment.DoesNotExist:
                apartment = Apartment.objects.first()
                context['default_apartment'] = apartment
                context['guest_max'] = apartment.guest_count
        else:
            apartment = Apartment.objects.first()
            context['default_apartment'] = apartment
            context['guest_max'] = apartment.guest_count

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
                if booking.check_out_date > datetime.today().date():
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
                    if client_value == PAYMENT_METHOD_CHOICES[0][0] and settings.ONLINE_PAYMENT == False:
                        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_payment_method']}, status=400)
            guest_data = data.get('guestData', [])
            for guest in guest_data:
                if not type(guest) is dict:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save(commit=False)

            if self.check_available_date(client_data) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['unavailable_period']})

            if self.check_guest_count(guest_data, booking_instance) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

            if self.check_price(client_data) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

            if self.check_privacy_policy(client_data) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_privacy_policy']}, status=400)

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
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

    def send_mailing(self, booking_instance):
        if booking_instance.payment_method == PAYMENT_METHOD_CHOICES[1][0]:
            threading.Thread(target=send_mail_for_admin,
                             args=('mailing/admin_callback.html', {
                                 'name': booking_instance.client_name,
                                 'phone': booking_instance.client_phone,
                                 'created': booking_instance.created_at
                             })).start()
        if booking_instance.payment_method == PAYMENT_METHOD_CHOICES[0][0]:
            threading.Thread(target=send_mail_for_client,
                             args=(booking_instance.client_mail, 'mailing/client_receipt.html', {
                                 'name': booking_instance.client_name,
                                 'check_in': booking_instance.check_in_date,
                                 'check_out': booking_instance.check_out_date,
                                 'is_paid': booking_instance.is_paid,
                                 'total_sum': booking_instance.total_sum
                             })).start()

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
                if int(apartment) == booking.apartment:
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
        if 0 < len(guest_data) <= Apartment.objects.get(id=booking_instance.apartment).guest_count:
            if len(guest_data) != booking_instance.guests_count:
                return False
        else:
            return False
        return True

    def check_privacy_policy(self, client_data):
        if not client_data["is_privacy_policy"]:
            return False
        return True
