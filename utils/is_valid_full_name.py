def is_valid_full_name(name, surname, father_name):
    if not name or not surname or not father_name:
        return False
    if not name.isalpha() or not surname.isalpha() or not father_name.isalpha():
        return False
    if len(name) < 2 or len(surname) < 2 or len(father_name) < 2:
        return False
    return True
