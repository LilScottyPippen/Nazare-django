import re


def is_valid_phone(phone):
    phone = str(phone)
    belarus_pattern = r'^(?:\+375|375)\d{9}$'
    russia_pattern = r'^(?:\+7|7)\d{10}$'
    if re.match(belarus_pattern, phone) or re.match(russia_pattern, phone):
        return True
    return False
