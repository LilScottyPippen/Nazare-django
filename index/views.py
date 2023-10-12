import os
import re
import threading
from .models import *
from .constants import *
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseNotFound
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class IndexPageView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageType'] = "Главная страница"
        return context


class DevelopPageView(TemplateView):
    template_name = 'index/development.html'

    def get_context_data(self, **kwargs):
        description = DEVELOP_DESCRIPTION.get(kwargs['pageType'], '')

        context = super().get_context_data(**kwargs)
        context['description'] = description
        context['pageType'] = "Страница в разработке"
        return context


class PrivacyPageView(TemplateView):
    template_name = 'index/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageType'] = "Политика конфиденциальности"
        return context


class CatalogPageView(View):
    def get(self, request, **kwargs):
        try:
            category = Category.objects.get(slug=kwargs.get('pageType').lower())
            subcategories = Subcategory.objects.filter(category=category)
            title = category.title
            if request.LANGUAGE_CODE == "en":
                title = category.title_en

            context = {
                'page_url': 'apartHomePage',
                'pageType': title,
                'subcategories': subcategories,
            }
            return render(request, 'index/catalog.html', context)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Page not found")


class ApartHomePageView(View):
    def get(self, request, **kwargs):
        try:
            apartment = Apartment.objects.get(title=kwargs.get('title'))
            image_folder_path = os.path.join(settings.STATIC_ROOT, 'img', 'apartments', apartment.title)

            image_files = os.listdir(image_folder_path)
            home_title = f'ДОМ {apartment.title.upper()}'
            share_title = f'Забронировать дом {apartment.title.upper()}'
            if request.LANGUAGE_CODE == "en":
                home_title = f'{apartment.title.upper()} HOME'
                share_title = f'Book an {apartment.title.upper()} house'

            context = {
                'homeTitle': home_title,
                'homeGuests': apartment.guests,
                'homeSquare': apartment.square,
                'homeSleep': apartment.sleepPlace,
                'homePrice': apartment.dailyPrice,
                'imageFolderPath': image_folder_path,
                'imageFiles': image_files,
                'homeSlug': apartment.title,
                'homeShare': share_title,
                'pageType': f'Дом {apartment.title}'
            }
            return render(request, 'index/apartment-home.html', context)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Page not found")


class OrderCallView(View):
    def is_valid_phone(self, phone):
        belarus_pattern = r'^(?:\+375|375)\d{9}$'
        russia_pattern = r'^(?:\+7|7)\d{10}$'

        return re.match(belarus_pattern, phone) or re.match(russia_pattern, phone)

    def post(self, request):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        page_type = request.POST.get('pageType', '')

        if not name or not phone:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_name' if not name else 'empty_phone']})

        if any(char.isdigit() for char in name):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_name']})

        if any(char.isalpha() for char in phone) or not self.is_valid_phone(phone):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})

        try:
            callback = Callback.objects.create(name=name, phone=phone, placeApplication=page_type)
            threading.Thread(target=self.create_callback, args=(callback.id,)).start()
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_callback']})
        except Exception as e:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})

    def create_callback(self, callback_id):
        try:
            callback = Callback.objects.get(id=callback_id)
            message = render_to_string('mailing/admin_callback.html',
                                       {'name': callback.name, 'phone': callback.phone, 'created': callback.created_at})
            recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
            send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
            return True
        except Exception as e:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})


class ContactsPageView(TemplateView):
    template_name = 'index/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageType'] = "Контакты"
        return context


class SaveEmailView(View):
    def post(self, request):
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


class ServicePageView(View):
    def get(self, request, **kwargs):
        try:
            service = Services.objects.get(slug=kwargs.get('slug'))
            image_folder_path = os.path.join(settings.STATIC_ROOT, 'img', 'services', service.slug)
            image_files = os.listdir(image_folder_path)

            title = service.title.upper()
            description = service.description
            if request.LANGUAGE_CODE == "en":
                title = service.title_en.upper()
                description = service.description_en

            context = {
                'title': title,
                'slug': service.slug,
                'desc': description,
                'imageFiles': image_files,
                'pageType': service.title
            }
            return render(request, 'index/service.html', context)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Page not found")


class GalleryPageView(View):
    def get(self, request, category):
        folder_path = 'img/territory'
        title = _('ТЕРРИТОРИЯ')

        categories = list(Apartment.objects.values_list('title', flat=True))

        if category in categories:
            folder_path = 'img/apartments/' + category
            title = f'ДОМ {category.upper()}'
            if request.LANGUAGE_CODE == "en":
                title = f'{category.upper()} HOME'

        full_folder_path = os.path.join(settings.STATICFILES_DIRS[0], folder_path)

        image_paths = []
        for filename in os.listdir(full_folder_path):
            img_path = os.path.join(folder_path, filename)
            image_paths.append(img_path)

        context = {
            'image_paths': image_paths,
            'page_title': title,
            'pageType': title
        }
        return render(request, 'index/gallery.html', context)


class RentPageView(TemplateView):
    template_name = 'index/rent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
