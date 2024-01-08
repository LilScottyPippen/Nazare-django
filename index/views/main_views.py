from django.views.generic import TemplateView
from index.models import *


class IndexPageView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = ApartmentMenu.objects.all()
        return context


class ApartmentPageView(TemplateView):
    template_name = "index/apartment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartment = Apartment.objects.get(
            slug=kwargs['apartment'])

        context["apartment"] = apartment
        context["price_lists"] = ApartmentPriceList.objects.filter(
            apartment=apartment)
        context["photos"] = ApartmentPhotoGallery.objects.filter(
            apartment=apartment)
        context["conveniences"] = ApartmentConvenience.objects.filter(
            apartment=apartment)
        context["first_photo"] = context["photos"].first()
        return context
