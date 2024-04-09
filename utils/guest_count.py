from index.models import Apartment


def get_max_guest_count():
    try:
        max_guests = Apartment.objects.all().order_by('-guest_count').first().guest_count
    except AttributeError:
        return False
    return max_guests


def check_correct_guest_count(count):
    max_guests = get_max_guest_count()

    if type(count) is not int:
        return False

    if count > max_guests or max_guests <= 0:
        return False
    return True


def check_guest_count_limit(count, limit):
    if type(count) is not int:
        return False

    if count > limit:
        return False

    return True
