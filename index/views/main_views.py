import json
import random
import threading
from django.http import JsonResponse, Http404
from django.views import View
from django.views.generic import TemplateView
import folium
from index.models import ApartmentMenu, ContactPage, Address, Email, Phone, Content
from utils.constants import *
from utils.get_max_guest_count import get_max_guest_count
from ..forms.subscriber_form import *
from ..forms.callback_form import *
from utils.send_mail import send_mail_for_admin, send_mail_for_client
from django.utils import timezone
from datetime import datetime


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


class SubscriberView(View):
    def post(self, request, **kwargs):
        client_mail = request.POST.get('mail')
        captcha_response = request.POST.get('captcha')

        if len(captcha_response) == 0:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_captcha']}, status=500)

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_subscribed']}, status=200)
        else:
            if Subscriber.objects.filter(mail=client_mail):
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_mail']}, status=500)
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)


class CallbackView(View):
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            client_data = data.get('client_data', {})

            for client_key, client_value in client_data.items():
                if client_key == 'phone' and is_valid_phone(client_value) is False:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_phone']}, status=500)
                if client_key == 'captcha' and len(client_value) == 0:
                    return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_captcha']}, status=500)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)

        form = CallbackForm(client_data)

        callback_context = {
            'name': client_data['name'],
            'phone': client_data['phone'],
            'created': datetime.now()
        }

        if form.is_valid():
            form.save()
            threading.Thread(target=send_mail_for_admin,
                             args=(MAILING_SUBJECTS['callback_admin'], 'mailing/admin_callback.html', callback_context)).start()
            return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_callback']}, status=200)
        return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_form']}, status=500)


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


class SendConfirmationCodeView(View):
    def get(self, request, mail):
        last_request_time_str = request.session.get('last_confirmation_code_request_time')
        if last_request_time_str:
            last_request_time = datetime.strptime(last_request_time_str, "%Y-%m-%d %H:%M:%S.%f")
            if (timezone.now() - last_request_time).seconds < 60:
                return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['code_request_too_soon']}, status=200)

        confirmation_code = ''.join(str(random.randint(0, 9)) for _ in range(6))

        try:
            request.session['confirmation_code'] = confirmation_code
            request.session['last_confirmation_code_request_time'] = str(timezone.now())
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['invalid_send_code']}, status=500)

        threading.Thread(target=send_mail_for_client,
                         args=(MAILING_SUBJECTS['confirm_email'], mail, 'mailing/confirmation_code.html',
                               {'code': confirmation_code})).start()

        return JsonResponse({'status': 'success', 'message': SUCCESS_MESSAGES['success_send_code']}, status=200)


class ConfirmEmailView(View):
    def get(self, request, confirmation_code):
        saved_confirmation_code = request.session.get('confirmation_code')
        if saved_confirmation_code == confirmation_code:
            del request.session['confirmation_code']
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': ERROR_MESSAGES['incorrect_code']}, status=500)