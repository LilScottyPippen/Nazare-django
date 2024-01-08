from django.views.generic import TemplateView
import folium
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


class ContactPageView(TemplateView):
    template_name = "index/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map = folium.Map(
            [55.255200, 30.162598], zoom_start=12)
        folium.Marker([55.255200, 30.162598], popup="Зорька").add_to(map)
        contact = ContactPage.objects.all().first()
        context['map'] = map._repr_html_()
        context['adresses'] = Address.objects.filter(contact=contact)
        context['emails'] = Email.objects.filter(contact=contact)
        context['telephones'] = Telephone.objects.filter(contact=contact)
        return context
