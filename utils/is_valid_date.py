import datetime


def is_valid_date_booking(check_in, check_out):
    if datetime.date.today() <= check_in < check_out:
        return True


