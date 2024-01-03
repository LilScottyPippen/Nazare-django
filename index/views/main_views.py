from django.views.generic import TemplateView
import folium
from index.models import *


class IndexPageView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = ApartamentMenu.objects.all()
        return context


class ApartamentPageView(TemplateView):
    template_name = "index/apartament.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartament = Apartament.objects.get(
            slug=kwargs['apartament'])

        context["apartament"] = apartament
        context["price_lists"] = ApartamentPriceList.objects.filter(
            apartament=apartament)
        context["photos"] = ApartamentPhotoGalery.objects.filter(
            apartament=apartament)
        context["conveniences"] = ApartamentConvenience.objects.filter(
            apartament=apartament)
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
        context['telephones'] = Telephon.objects.filter(contact=contact)
        return context
