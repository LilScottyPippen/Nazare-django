import threading
from django.views.generic import TemplateView
from booking.models.booking import *
from index.models.apartments import *
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
        context['apartments'] = Apartment.objects.all()
        return context

    def post(self, request):
        try:
            data = json.loads(request.body)
            client_data = data.get('clientData', {})
            guest_data = data.get('guestData', [])
            for guest in guest_data:
                if not type(guest) is dict:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save()

            if self.check_guest_count(guest_data, booking_instance) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

            if self.check_price(client_data) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

            if self.check_privacy_policy(client_data) is False:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_privacy_policy']}, status=400)

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

    def check_price(self, client_data):
        try:
            first_date = datetime.strptime(client_data['check_in_date'], "%Y-%m-%d")
            second_date = datetime.strptime(client_data['check_out_date'], "%Y-%m-%d")
            days = (second_date - first_date).days
            daily_price = Apartment.objects.get(id=int(client_data["apartment"])).daily_price * days
        except ValueError:
            return False

        if int(client_data['total_sum']) != daily_price:
            return False
        return True

    def check_guest_count(self, guest_data, booking_instance):
        if len(guest_data) != booking_instance.guests_count:
            return False
        return True

    def check_privacy_policy(self, client_data):
        if not client_data["is_privacy_policy"]:
            return False
        return True
