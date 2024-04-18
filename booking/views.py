import os
import json
import threading
from datetime import datetime
from Nazare_django import settings
from django.views.generic import TemplateView
from index.models.apartments import Apartment
from utils.is_valid_phone import is_valid_phone
from utils.json_responses import error_response
from utils.is_valid_captcha import is_valid_captcha
from utils.booking import get_booking_in_range_date
from django.core.exceptions import PermissionDenied
from utils.guest_count import check_guest_count_limit
from .forms.booking_form import BookingForm, GuestsForm
from booking.models.booking import PAYMENT_METHOD_CHOICES
from django.http import JsonResponse, Http404, RawPostDataException
from utils.send_mail import send_mail_for_client, send_mail_for_admin
from utils.is_valid_date import check_correct_booking_period, is_valid_date_booking
from utils.constants import SUCCESS_MESSAGES, ERROR_MESSAGES, MAILING_SUBJECTS, DATE_FORMAT


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        context["online_payment"] = settings.ONLINE_PAYMENT

        apartment_id = self.request.GET.get('apartment')
        check_in_date = self.request.GET.get('check_in_date')
        check_out_date = self.request.GET.get('check_out_date')

        try:
            adult_count = int(self.request.GET.get('adult_count'))
            children_count = int(self.request.GET.get('children_count'))
        except (ValueError, TypeError):
            adult_count, children_count = 1, 0

        if apartment_id:
            try:
                try:
                    apartment = Apartment.objects.get(id=apartment_id)
                except ValueError:
                    raise Http404
            except Apartment.DoesNotExist:
                apartment = Apartment.objects.first()
        else:
            apartment = Apartment.objects.first()

        context['default_apartment'] = apartment

        try:
            context['guest_max'] = apartment.guest_count
        except AttributeError:
            raise PermissionDenied()

        if check_in_date and check_out_date:
            try:
                if type(check_in_date) is not datetime:
                    check_in_date = datetime.strptime(check_in_date, DATE_FORMAT['YYYY-MM-DD'])

                if type(check_out_date) is not datetime:
                    check_out_date = datetime.strptime(check_out_date, DATE_FORMAT['YYYY-MM-DD'])
            except (ValueError, TypeError):
                pass

            if is_valid_date_booking(check_in_date, check_out_date):
                check_in_date = check_in_date.strftime(DATE_FORMAT['YYYY-MM-DD'])
                check_out_date = check_out_date.strftime(DATE_FORMAT['YYYY-MM-DD'])

                bookings = get_booking_in_range_date(check_in_date, check_out_date)

                isBooked = False

                for booking in bookings:
                    if booking.apartment.id == int(apartment_id) and booking.confirmed:
                        isBooked = True

                if not isBooked:
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

            if client_data is None:
                return error_response(ERROR_MESSAGES['bad_request'])

            if 'captcha' not in client_data:
                return error_response(ERROR_MESSAGES['invalid_captcha'], status=500)

            for client_key, client_value in client_data.items():
                if client_key == 'payment_method':
                    if client_value == PAYMENT_METHOD_CHOICES[0][0] and not settings.ONLINE_PAYMENT:
                        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_payment_method']},
                                            status=500)
                if client_key == 'client_phone' and not is_valid_phone(client_value):
                    return error_response(ERROR_MESSAGES['invalid_phone'])
                if client_key == 'captcha' and not is_valid_captcha(client_value):
                    return error_response(ERROR_MESSAGES['invalid_captcha'])
                if client_key == 'guests_count' and int(client_value) <= 0:
                    return error_response(ERROR_MESSAGES['invalid_form'])
                if client_key == 'children_count' and int(client_value) < 0:
                    return error_response(ERROR_MESSAGES['invalid_form'])

            guest_data = data.get('guestData', [])
            for guest in guest_data:
                if not type(guest) is dict:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

        try:
            apartment = int(client_data['apartment'])

            try:
                check_in_date = datetime.strptime(client_data['check_in_date'], DATE_FORMAT['YYYY-MM-DD'])
                check_out_date = datetime.strptime(client_data['check_out_date'], DATE_FORMAT['YYYY-MM-DD'])
            except TypeError:
                return error_response(ERROR_MESSAGES["bad_request"])

            guests_count = int(client_data["guests_count"]) + int(client_data["children_count"])
            total_sum = int(client_data["total_sum"])
        except KeyError:
            return error_response(ERROR_MESSAGES["bad_request"])

        try:
            max_guest_count = Apartment.objects.get(id=apartment).guest_count
        except (Apartment.DoesNotExist, AttributeError):
            return error_response(ERROR_MESSAGES["bad_request"])

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save(commit=False)

            if not self.check_available_date(apartment, check_in_date, check_out_date):
                return error_response(ERROR_MESSAGES['unavailable_period'])

            if not check_correct_booking_period(check_in_date, check_out_date):
                return error_response(ERROR_MESSAGES['unavailable_period'])

            if len(guest_data) != int(client_data["guests_count"]):
                return error_response(ERROR_MESSAGES['invalid_form'])

            if not check_guest_count_limit(guests_count, max_guest_count):
                return error_response(ERROR_MESSAGES['invalid_form'])

            if not self.check_price(apartment, check_in_date, check_out_date, total_sum):
                return error_response(ERROR_MESSAGES['invalid_form'])

            if not self.check_privacy_policy(client_data):
                return error_response(ERROR_MESSAGES['invalid_privacy_policy'])

            booking_instance.save()
            self.send_mailing(booking_instance)

            for guest_form_data in guest_data:
                guest_form = GuestsForm(guest_form_data)
                if guest_form.is_valid():
                    guest_instance = guest_form.save(commit=False)
                    guest_instance.booking = booking_instance
                    guest_instance.save()

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

    def check_available_date(self, apartment, check_in_date, check_out_date):
        try:
            if type(check_in_date) is not datetime:
                check_in_date = datetime.strptime(check_in_date, DATE_FORMAT['YYYY-MM-DD'])

            if type(check_out_date) is not datetime:
                check_out_date = datetime.strptime(check_out_date, DATE_FORMAT['YYYY-MM-DD'])
        except TypeError:
            return False

        if not check_correct_booking_period(check_in_date, check_out_date):
            return False

        booking_dict = get_booking_in_range_date(check_in_date, check_out_date)
        if booking_dict is not False:
            for booking in booking_dict:
                if booking.confirmed and int(apartment) == booking.apartment.id:
                    return False
        else:
            return False
        return True

    def check_price(self, apartment, check_in_date, check_out_date, total_sum):
        if type(check_in_date) is not datetime and type(check_out_date) is not datetime:
            return False

        try:
            days = (check_out_date - check_in_date).days
            daily_price = Apartment.objects.get(id=int(apartment)).daily_price * days
        except (ValueError, KeyError, Apartment.DoesNotExist, AttributeError):
            return False

        if int(total_sum) != daily_price:
            return False
        return True

    def check_privacy_policy(self, client_data):
        if not client_data["is_privacy_policy"]:
            return False
        return True
