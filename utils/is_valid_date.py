import datetime


def is_valid_date_booking(check_in, check_out):
    if check_in is None or check_out is None:
        return False
    if datetime.date.today() <= check_in < check_out:
        return True
    return False
