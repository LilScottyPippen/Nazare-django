import os
import datetime
from utils.constants import DATE_FORMAT


def is_valid_date_booking(check_in, check_out):
    check_in_time_str = os.environ.get('CHECK_IN_TIME', '14:00')
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())

    try:
        check_in_time = datetime.datetime.strptime(check_in_time_str, DATE_FORMAT['HH-MM']).time()
    except ValueError:
        return False

    if check_in is None or check_out is None:
        return False

    try:
        if type(check_in) is not datetime.datetime and type(check_out) is not datetime.datetime:
            check_in = datetime.datetime.strptime(str(check_in), DATE_FORMAT['YYYY-MM-DD'])
            check_out = datetime.datetime.strptime(str(check_out), DATE_FORMAT['YYYY-MM-DD'])
    except TypeError:
        return False

    if not check_correct_booking_period(check_in, check_out):
        return False

    try:
        if today == check_in:
            if datetime.datetime.now().time() >= check_in_time:
                return False

        if today <= check_in < check_out:
            return True
    except TypeError:
        today = datetime.date.today()

        if today == check_in:
            if datetime.datetime.now().time() >= check_in_time:
                return False

        if today <= check_in < check_out:
            return True
    return False


def check_correct_booking_period(check_in, check_out):
    if type(check_in) is datetime.datetime and type(check_out) is datetime.datetime:
        if (check_out - check_in).days <= int(os.getenv("MAX_BOOKING_PERIOD")):
            return True
    return False
