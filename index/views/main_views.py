import folium
from django.http import Http404
from django.views.generic import TemplateView
from utils.guest_count import get_max_guest_count
from index.models import ApartmentMenu, ContactPage, Address, Email, Phone, Content


class IndexPageView(TemplateView):
    template_name = "index/index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = ApartmentMenu.objects.all()
        context["guest_max"] = get_max_guest_count()
        return context


class ContactPageView(TemplateView):
    template_name = "index/contact/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map = folium.Map(
            [55.255200, 30.162598], zoom_start=12)

        folium.Marker(
            location=[55.255200, 30.162598],
            popup=folium.Popup("Парк отель NA ZARE", max_width=165),
        ).add_to(map)

        contact = ContactPage.objects.all().first()
        context['map'] = map._repr_html_()
        context['addresses'] = Address.objects.filter(contact=contact)
        context['emails'] = Email.objects.filter(contact=contact)
        context['phones'] = Phone.objects.filter(contact=contact)
        return context


class ContentView(TemplateView):
    template_name = 'index/content/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['content'] = Content.objects.get(slug=kwargs.get('slug'))
        except Content.DoesNotExist:
            raise Http404
        return context


class PolicyView(TemplateView):
    template_name = 'index/policy/policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MaintenanceView(TemplateView):
    template_name = "index/maintenance/maintenance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
