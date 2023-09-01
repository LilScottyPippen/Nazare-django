import re
from .tasks import *
from .models import *
from .constants import *
from django.views import View
from django.conf import settings
from urllib.parse import urlparse
from django.shortcuts import render
from django.utils import translation
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


class SetLanguageView(View):
    def get(self, request, language):
        referer = request.META.get("HTTP_REFERER", "/")
        referer_path = urlparse(referer).path
        try:
            view = resolve(referer_path)
        except Resolver404:
            view = None

        if view:
            translation.activate(language)
            url_name = getattr(view, 'url_name', None)
            args = getattr(view, 'args', [])
            kwargs = getattr(view, 'kwargs', {})
            next_url = reverse(url_name, args=args, kwargs=kwargs) if url_name else "/"
        else:
            next_url = "/"

        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response


class IndexPageView(View):
    def get(self, request):
        current_language = request.LANGUAGE_CODE

        context = {
            'cur_lang': current_language
        }
        return render(request, 'index/index.html', context)


class DevelopPageView(View):
    def get(self, request, pageType):
        current_language = request.LANGUAGE_CODE
        description = DEVELOP_DESCRIPTION.get(pageType, '')

        context = {
            'cur_lang': current_language,
            'description': description
        }
        return render(request, 'index/development.html', context)


class PrivacyPageView(View):
    def get(self, request):
        current_language = request.LANGUAGE_CODE

        context = {
            'cur_lang': current_language,
        }
        return render(request, 'index/privacy.html', context)


class ApartmentsPageView(View):
    def get(self, request):
        current_language = request.LANGUAGE_CODE

        context = {
            'cur_lang': current_language,
        }
        return render(request, 'index/apartments.html', context)


class ApartHomePageView(View):
    def get(self, request, title):
        current_language = request.LANGUAGE_CODE

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
                'cur_lang': current_language,
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

    def post(self, request):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')

        if not name or not phone:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_name' if not name else 'empty_phone']})

        if any(char.isdigit() for char in name):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_name']})

        if any(char.isalpha() for char in phone):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})

        if not self.is_valid_phone(phone):
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})

        try:
            callback = Callback.objects.create(name=name, phone=phone)
            create_callback.delay(callback.id)
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_callback']})
        except Exception as e:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})


class ContactsPageView(View):
    def get(self, request):
        current_language = request.LANGUAGE_CODE

        context = {
            'cur_lang': current_language,
        }
        return render(request, 'index/contacts.html', context)


@csrf_exempt
def save_email(request):
    try:
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

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# def rent_page(request):
#     current_language = request.LANGUAGE_CODE

#     context = {
#         'cur_lang': current_language
#     }
#     return render(request, 'index/rent.html', context)


class TerritoryPageView(View):
    def get(self, request):
        current_language = request.LANGUAGE_CODE

        folder_path = 'img/territory'
        full_folder_path = os.path.join(settings.STATICFILES_DIRS[0], folder_path)

        image_paths = []
        for filename in os.listdir(full_folder_path):
            img_path = os.path.join(folder_path, filename)
            image_paths.append(img_path)

        context = {
            'cur_lang': current_language,
            'image_paths': image_paths
        }
        return render(request, 'index/territoryGallery.html', context)
