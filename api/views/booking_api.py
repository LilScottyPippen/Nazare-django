import os
import json
import threading
from django.views import View
from datetime import datetime
from Nazare_django import settings
from index.models import Apartment
from utils.is_valid_phone import is_valid_phone
from django_ratelimit.decorators import ratelimit
from utils.booking import get_booking_in_range_date
from django.utils.decorators import method_decorator
from django.http import JsonResponse, RawPostDataException
from utils.is_valid_captcha import is_valid_session_captcha
from utils.is_valid_date import check_correct_booking_period
from booking.forms.booking_form import BookingForm, GuestsForm
from utils.json_responses import error_response, success_response
from booking.models.booking import Booking, PAYMENT_METHOD_CHOICES
from utils.send_mail import send_mail_for_admin, send_mail_for_client
from utils.guest_count import get_max_guest_count, check_guest_count_limit
from utils.constants import ERROR_MESSAGES, DATE_FORMAT, CAPTCHA_SUBJECT, SUCCESS_MESSAGES, MAILING_SUBJECTS


class BookingAPIView(View):
    @method_decorator(ratelimit(key='ip', rate='10/m'))
    def post(self, request):
        try:
            try:
                data = json.loads(request.body)
            except RawPostDataException:
                return error_response(ERROR_MESSAGES['bad_request'])

            client_data = data.get('clientData')

            if client_data is None:
                return error_response(ERROR_MESSAGES['bad_request'])

            if not is_valid_session_captcha(request, CAPTCHA_SUBJECT['booking_captcha']):
                return error_response(ERROR_MESSAGES['invalid_captcha'])

            for client_key, client_value in client_data.items():
                if client_key == 'payment_method':
                    if client_value == PAYMENT_METHOD_CHOICES[0][0] and not settings.ONLINE_PAYMENT:
                        return error_response(ERROR_MESSAGES['invalid_payment_method'])
                if client_key == 'client_phone' and not is_valid_phone(client_value):
                    return error_response(ERROR_MESSAGES['invalid_phone'])
                if client_key == 'guests_count' and int(client_value) <= 0:
                    return error_response(ERROR_MESSAGES['invalid_form'])
                if client_key == 'children_count' and int(client_value) < 0:
                    return error_response(ERROR_MESSAGES['invalid_form'])

            guest_data = data.get('guestData', [])
            for guest in guest_data:
                if not type(guest) is dict:
                    return error_response(ERROR_MESSAGES['invalid_form'])
        except ValueError:
            return error_response(ERROR_MESSAGES['invalid_form'])

        try:
            apartment_id = int(client_data['apartment'])

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
            max_guest_count = Apartment.objects.get(id=apartment_id).guest_count
        except (Apartment.DoesNotExist, AttributeError):
            return error_response(ERROR_MESSAGES["bad_request"])

        form = BookingForm(client_data)

        if form.is_valid():
            booking_instance = form.save(commit=False)

            if not self.check_available_date(apartment_id, check_in_date, check_out_date):
                return error_response(ERROR_MESSAGES['unavailable_period'])

            if not check_correct_booking_period(check_in_date, check_out_date):
                return error_response(ERROR_MESSAGES['unavailable_period'])

            if len(guest_data) != int(client_data["guests_count"]):
                return error_response(ERROR_MESSAGES['invalid_form'])

            if not check_guest_count_limit(guests_count, max_guest_count):
                return error_response(ERROR_MESSAGES['invalid_form'])

            if not self.check_price(apartment_id, check_in_date, check_out_date, total_sum):
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

            return success_response(SUCCESS_MESSAGES['success_booking'])
        else:
            return error_response(ERROR_MESSAGES['invalid_form'])

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

    def check_available_date(self, apartment_id, check_in_date, check_out_date):
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
                if booking.confirmed and int(apartment_id) == booking.apartment.id:
                    return False
        else:
            return False
        return True

    def check_price(self, apartment_id, check_in_date, check_out_date, total_sum):
        if type(check_in_date) is not datetime and type(check_out_date) is not datetime:
            return False

        try:
            days = (check_out_date - check_in_date).days
            daily_price = Apartment.objects.get(id=int(apartment_id)).daily_price * days
        except (ValueError, KeyError, Apartment.DoesNotExist, AttributeError):
            return False

        if int(total_sum) != daily_price:
            return False
        return True

    def check_privacy_policy(self, client_data):
        if client_data["is_privacy_policy"] is not True:
            return False
        return True


class BookingListAPIView(View):
    def get(self, request):
        apartment_dict = Apartment.objects.all()
        booking_list = self.creating_booking_list(apartment_dict)

        if not booking_list:
            return error_response(ERROR_MESSAGES['bad_request'])
        return JsonResponse(booking_list, safe=False, status=200)

    def creating_booking_list(self, apartment_dict):
        booking_list = {}

        for apartment in apartment_dict:
            try:
                booking_list[apartment.id] = []
            except (Apartment.DoesNotExist, AttributeError):
                return False
            for booking in Booking.objects.filter(apartment=apartment.id):
                if booking.check_out_date >= datetime.today().date() and booking.confirmed:
                    booking_list[apartment.id].append([
                        booking.check_in_date.strftime(DATE_FORMAT['YYYY-MM-DD']),
                        booking.check_out_date.strftime(DATE_FORMAT['YYYY-MM-DD'])
                    ])
        return booking_list


class GuestMaxAPIView(View):
    def get(self, request):
        guest_max = int(get_max_guest_count())

        if not guest_max:
            return error_response(ERROR_MESSAGES['bad_request'])
        return JsonResponse({'guest_max': guest_max}, safe=False, status=200)


class GuestMaxApartmentAPIView(View):
    def get(self, request, apartment_id):
        try:
            apartment = Apartment.objects.get(id=apartment_id)
        except Apartment.DoesNotExist:
            return error_response(ERROR_MESSAGES['apartment_not_found'], 404)
        return JsonResponse({'guest_max': apartment.guest_count}, safe=False, status=200)


class CheckInTimeAPIView(View):
    def get(self, request):
        check_in_time = os.getenv('CHECK_IN_TIME')

        if not check_in_time:
            return error_response(ERROR_MESSAGES['bad_request'])
        return JsonResponse({'check_in_time': check_in_time}, safe=False, status=200)


class CheckOutTimeAPIView(View):
    def get(self, request):
        check_out_time = os.getenv('CHECK_OUT_TIME')

        if not check_out_time:
            return error_response(ERROR_MESSAGES['bad_request'])
        return JsonResponse({'check_out_time': check_out_time}, safe=False, status=200)


class MaxBookingPeriodAPIView(View):
    def get(self, request):
        booking_period = int(os.getenv('MAX_BOOKING_PERIOD'))

        if not booking_period:
            return error_response(ERROR_MESSAGES['bad_request'])
        return JsonResponse({'booking_period': booking_period}, safe=False, status=200)