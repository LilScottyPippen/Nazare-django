from datetime import datetime
from django.http import Http404
from Nazare_django import settings
from utils.constants import DATE_FORMAT
from .forms.booking_form import BookingForm
from django.views.generic import TemplateView
from index.models.apartments import Apartment
from utils.booking import check_available_apartment
from django.core.exceptions import PermissionDenied
from utils.guest_count import check_guest_count_limit
from utils.is_valid_date import is_valid_date_booking


class BookingView(TemplateView):
    template_name = 'booking/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_form"] = BookingForm()
        context["online_payment"] = settings.ONLINE_PAYMENT

        apartment_id = self.request.GET.get('apartment')
        check_in_date = self.request.GET.get('check_in_date')
        check_out_date = self.request.GET.get('check_out_date')

        try:
            adult_count = int(self.request.GET.get('adult_count'))
            children_count = int(self.request.GET.get('children_count'))
        except (ValueError, TypeError):
            adult_count, children_count = 1, 0

        if apartment_id:
            try:
                try:
                    apartment = Apartment.objects.get(id=apartment_id)
                except ValueError:
                    raise Http404
            except Apartment.DoesNotExist:
                apartment = Apartment.objects.first()
        else:
            apartment = Apartment.objects.first()

        context['default_apartment'] = apartment

        try:
            context['guest_max'] = apartment.guest_count
        except AttributeError:
            raise PermissionDenied()

        if check_in_date and check_out_date:
            try:
                if type(check_in_date) is not datetime:
                    check_in_date = datetime.strptime(check_in_date, DATE_FORMAT['YYYY-MM-DD'])

                if type(check_out_date) is not datetime:
                    check_out_date = datetime.strptime(check_out_date, DATE_FORMAT['YYYY-MM-DD'])
            except (ValueError, TypeError):
                pass

            if is_valid_date_booking(check_in_date, check_out_date):
                check_in_date = check_in_date.strftime(DATE_FORMAT['YYYY-MM-DD'])
                check_out_date = check_out_date.strftime(DATE_FORMAT['YYYY-MM-DD'])

                if check_available_apartment(apartment.id, check_in_date, check_out_date):
                    context['check_in_date'] = check_in_date
                    context['check_out_date'] = check_out_date

        if check_guest_count_limit(adult_count + children_count, apartment.guest_count):
            context['adult_count'] = adult_count
            context['children_count'] = children_count

        context['apartments'] = Apartment.objects.all()
        return context
