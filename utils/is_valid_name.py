def is_valid_name(*args):
    for i in args:
        i = str(i)
        if not i.isalpha() or len(i) < 2:
            return False
    return True
