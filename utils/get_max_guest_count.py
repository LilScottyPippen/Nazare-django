from index.models import Apartment


def get_max_guest_count():
    apartment_dict = Apartment.objects.all()
    max_guests = apartment_dict[0].guest_count
    for apartment in apartment_dict:
        guest_count = apartment.guest_count
        if guest_count > max_guests:
            max_guests = guest_count
    return max_guests
