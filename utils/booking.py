from django.apps import apps
from django.db.models import Q
from django.core.exceptions import ValidationError


def get_booking_in_range_date(check_in_date, check_out_date):
    try:
        booking = apps.get_model('booking', 'Booking')
        booking_dict = booking.objects.filter(
            Q(check_in_date__range=[check_in_date, check_out_date]) |
            Q(check_out_date__range=[check_in_date, check_out_date])
        )
        return booking_dict
    except ValidationError:
        return False
