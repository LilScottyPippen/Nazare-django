import datetime
from django.http import Http404
from django.views.generic import TemplateView
from index.models import Apartment, ApartmentPhotoGallery, ApartmentMenu
from booking.models.booking import Booking
from utils.booking import get_booking_in_range_date
from utils.constants import ERROR_MESSAGES
from utils.guest_count import get_max_guest_count, check_correct_guest_count
from utils.is_valid_date import is_valid_date_booking


class ApartmentPageView(TemplateView):
    template_name = "index/apartment/apartment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            apartment = Apartment.objects.get(slug=kwargs['apartment'])
        except Apartment.DoesNotExist:
            raise Http404
        context["apartment"] = apartment
        try:
            context["included_services"] = apartment.includedService_package.included_services.all()
        except AttributeError:
            context["included_services"] = []
        context["photos"] = ApartmentPhotoGallery.objects.filter(apartment=apartment)
        try:
            context["conveniences"] = apartment.convenience_package.conveniences.all()
        except AttributeError:
            context["conveniences"] = []
        context["first_photo"] = context["photos"].first()
        return context


class ApartmentSearchView(TemplateView):
    template_name = "index/apartment/apartment_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check_in_date, check_out_date = kwargs.get('check_in_date'), kwargs.get('check_out_date')

        adult_count, children_count = int(kwargs.get('adult_count')), int(kwargs.get('children_count'))

        adult_count = adult_count if check_correct_guest_count(adult_count) else 1
        children_count = children_count if check_correct_guest_count(children_count) else 0

        apartment_dict = Apartment.objects.all()

        total_guests = adult_count + children_count

        if total_guests > get_max_guest_count():
            adult_count, children_count = 1, 0
            total_guests = adult_count + children_count

        try:
            check_in_date_formatted = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out_date_formatted = datetime.datetime.strptime(check_out_date, "%Y-%m-%d")
        except ValueError:
            raise Http404(ERROR_MESSAGES['invalid_date'])

        current_date = datetime.date.today()

        if check_out_date_formatted.date() > check_in_date_formatted.date() >= current_date:
            booking_dict = self.get_available_apartments_for_date_availability(
                apartment_dict,
                check_in_date_formatted,
                check_out_date_formatted
            )

            if booking_dict is not False:
                if len(booking_dict) <= apartment_dict.count():
                    available_apartments = self.get_available_apartments_for_guest_count(booking_dict, total_guests)
                    if available_apartments:
                        context["apartments"] = ApartmentMenu.objects.filter(apartment_id__in=available_apartments)

        context['check_in_date'] = check_in_date
        context['check_out_date'] = check_out_date
        context["days"] = (check_out_date_formatted - check_in_date_formatted).days
        context["adult_count"] = adult_count
        context["children_count"] = children_count
        return context

    def get_available_apartments_for_guest_count(self, booking_list, guest_count):
        try:
            apartment_dict_in_range = Apartment.objects.filter(
                guest_count__range=[guest_count, get_max_guest_count()])
        except ValueError:
            return False

        available_apartments = []

        for apartment in apartment_dict_in_range:
            if apartment.id in booking_list:
                available_apartments.append(apartment.id)
        return available_apartments

    def get_available_apartments_for_date_availability(self, apartment_dict, check_in_date, check_out_date):
        apartments_list, available_apartments = {}, []

        for apartment in apartment_dict:
            apartments_list[apartment.id] = 0
        if not is_valid_date_booking(check_in_date, check_out_date):
            return False
        booking_dict = get_booking_in_range_date(check_in_date, check_out_date)
        if booking_dict is not False:
            for booking in booking_dict:
                if booking.confirmed:
                    apartment_from_booking = Apartment.objects.filter(id=Booking.objects.get(id=booking.id).apartment.id)
                    apartments_list[apartment_from_booking.get().id] += 1

            for apartment in apartments_list:
                if apartments_list[apartment] == 0:
                    available_apartments.append(apartment)
            return available_apartments
        else:
            return False
