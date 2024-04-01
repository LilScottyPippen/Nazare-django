def is_valid_full_name(name, surname, *args):
    if not name or not surname:
        return False
    if not name.isalpha() or not surname.isalpha():
        return False
    if len(name) < 2 or len(surname) < 2:
        return False

    for i in args:
        if not i.isalpha():
            return False
        if not len(i) < 2:
            return False

    return True
