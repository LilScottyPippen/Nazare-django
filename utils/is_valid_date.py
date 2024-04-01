import datetime
import os


def is_valid_date_booking(check_in, check_out):
    check_in_time_str = os.environ.get('CHECK_IN_TIME', '14:00')
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())

    try:
        check_in_time = datetime.datetime.strptime(check_in_time_str, '%H:%M').time()
    except ValueError:
        return False

    if check_in is None or check_out is None:
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
