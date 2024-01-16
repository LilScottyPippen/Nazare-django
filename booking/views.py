import threading
from django.views.generic import TemplateView
from .models.booking import *
from index.models.apartments import *
from .forms.booking_form import *
from utils.send_mail import *
import json
from django.http import JsonResponse
from utils.constants import *


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
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save()

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
