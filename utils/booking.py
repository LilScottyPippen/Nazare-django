from datetime import datetime
from index.models import Apartment
from utils.constants import DATE_FORMAT
from booking.models import Booking, MultiApartmentBooking
from utils.is_valid_date import check_correct_booking_period


def creating_booking_list(apartment_dict):
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

    for booking in MultiApartmentBooking.objects.all():
        apartment_list = booking.apartments.values_list('id', flat=True)
        for apartment in apartment_list:
            if apartment not in booking_list:
                booking_list[apartment] = []

            if booking.check_out_date >= datetime.today().date():
                booking_list[apartment].append([
                    booking.check_in_date.strftime(DATE_FORMAT['YYYY-MM-DD']),
                    booking.check_out_date.strftime(DATE_FORMAT['YYYY-MM-DD'])
                ])
    return booking_list


def check_available_apartment(apartment_id, check_in_date, check_out_date):
    try:
        if type(check_in_date) is not datetime:
            check_in_date = datetime.strptime(check_in_date, DATE_FORMAT['YYYY-MM-DD'])

        if type(check_out_date) is not datetime:
            check_out_date = datetime.strptime(check_out_date, DATE_FORMAT['YYYY-MM-DD'])
    except TypeError:
        return False

    if not check_correct_booking_period(check_in_date, check_out_date):
        return False

    booking_dict = creating_booking_list([Apartment.objects.get(id=apartment_id)])

    for apartment, bookings in booking_dict.items():
        if apartment == apartment_id:
            for booking in bookings:
                booking_start = datetime.strptime(booking[0], DATE_FORMAT['YYYY-MM-DD'])
                booking_end = datetime.strptime(booking[1], DATE_FORMAT['YYYY-MM-DD'])

                if (check_in_date <= booking_start <= check_out_date) or \
                        (check_in_date <= booking_end <= check_out_date):
                    return False
    return True
