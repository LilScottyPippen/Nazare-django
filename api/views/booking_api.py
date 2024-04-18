import os
from django.views import View
from datetime import datetime
from index.models import Apartment
from django.http import JsonResponse
from booking.models.booking import Booking
from utils.constants import ERROR_MESSAGES
from utils.json_responses import error_response
from utils.guest_count import get_max_guest_count


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
                        booking.check_in_date.strftime("%Y-%m-%d"),
                        booking.check_out_date.strftime("%Y-%m-%d")
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