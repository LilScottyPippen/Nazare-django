import json
from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView
import folium
from index.models import *
from utils.constants import *
from utils.get_max_guest_count import get_max_guest_count
from ..forms.subscriber_form import *
from ..forms.callback_form import *


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
        context['telephones'] = Telephone.objects.filter(contact=contact)
        return context


class SubscriberView(View):
    def post(self, request, **kwargs):
        client_mail = request.POST.get('mail')
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_subscribed']}, status=200)
        else:
            if Subscriber.objects.filter(mail=client_mail):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_mail']}, status=400)
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)


class CallbackView(View):
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            client_data = data.get('client_data', {})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)

        form = CallbackForm(client_data)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_callback']}, status=200)
        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=400)


class ContentView(TemplateView):
    template_name = 'index/content/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['content'] = Content.objects.get(slug=kwargs.get('slug'))
        except Content.DoesNotExist:
            raise Http404
        return context
