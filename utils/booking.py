from django.db.models import Q
from booking.models.booking import Booking
from django.core.exceptions import ValidationError


def get_booking_in_range_date(check_in_date, check_out_date):
    try:
        booking_dict = Booking.objects.filter(
            Q(check_in_date__range=[check_in_date, check_out_date]) |
            Q(check_out_date__range=[check_in_date, check_out_date])
        )
    except ValidationError:
        return False
    return booking_dict
