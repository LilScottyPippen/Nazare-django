import re
from .tasks import *
from .models import *
from .constants import *
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class IndexPageView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DevelopPageView(TemplateView):
    template_name = 'index/development.html'

    def get_context_data(self, **kwargs):
        description = DEVELOP_DESCRIPTION.get(kwargs['pageType'], '')

        context = super().get_context_data(**kwargs)
        context['description'] = description
        return context


class PrivacyPageView(TemplateView):
    template_name = 'index/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApartmentsPageView(TemplateView):
    template_name = 'index/apartments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApartHomePageView(View):
    def get(self, request, title, *args, **kwargs):
        if title in HOME_TITLE:
            apartment = Apartment.objects.get(title=title)
            image_folder_path = os.path.join(settings.STATIC_ROOT, 'img', 'apartments', title)
            image_files = os.listdir(image_folder_path)
            context = {
                'homeTitle': HOME_TITLE[title],
                'homeGuests': apartment.guests,
                'homeSquare': apartment.square,
                'homeSleep': apartment.sleepPlace,
                'homeWiFi': apartment.isWifi,
                'imageFolderPath': image_folder_path,
                'imageFiles': image_files,
                'title': title,
                'homeShare': SHARE_APART_PAGE[title]
            }
            return render(request, 'index/apartment-home.html', context)
        return render(request, 'index/development.html')


class OrderCallView(View):
    def is_valid_phone(self, phone):
        belarus_pattern = r'^(?:\+375|375)?\d{9}$'
        russia_pattern = r'^(?:\+7|7)?\d{10}$'

        return re.match(belarus_pattern, phone) or re.match(russia_pattern, phone)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')

        if not name or not phone:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_name' if not name else 'empty_phone']})

        if any(char.isdigit() for char in name):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_name']})

        if any(char.isalpha() for char in phone) or not self.is_valid_phone(phone):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})

        try:
            callback = Callback.objects.create(name=name, phone=phone)
            create_callback.delay(callback.id)
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_callback']})
        except Exception as e:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})


class ContactsPageView(TemplateView):
    template_name = 'index/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SaveEmailView(View):
    def post(self, request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})

        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_email']})

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_email']})

        mail, created = Mail.objects.get_or_create(address=email)

        if created:
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_mailing']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['exists_email']})


class RentPageView(TemplateView):
    template_name = 'index/rent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TerritoryPageView(View):
    def get(self, request, *args, **kwargs):
        folder_path = 'img/territory'
        full_folder_path = os.path.join(settings.STATICFILES_DIRS[0], folder_path)

        image_paths = []
        for filename in os.listdir(full_folder_path):
            img_path = os.path.join(folder_path, filename)
            image_paths.append(img_path)

        context = {
            'image_paths': image_paths
        }
        return render(request, 'index/territoryGallery.html', context)
