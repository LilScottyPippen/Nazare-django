import os
import re
from .tasks import *
from .models import *
from django.conf import settings
from urllib.parse import urlparse
from django.shortcuts import render
from django.utils import translation
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

ERROR_MESSAGES = {
    'invalid_request': _('Недействительный запрос! Попробуйте еще раз.'),

    # CALLBACK
    'empty_name': _("Поле 'Ваше имя': пустое!"),
    'empty_phone': _("Поле 'Телефон': пустое!"),
    'invalid_name': _('Введите корректное имя!'),
    'invalid_phone': _('Введите корректный номер!'),

    # Mailing
    'empty_email': _("Поле 'Email': пустое!"),
    'invalid_email': _('Неверный адрес электронной почты!'),
    'exists_email': _("Электронная почта уже добавлена")
}

SUCCESS_MESSAGES = {
    # CALLBACK
    'success_callback': _("Спасибо за Вашу заявку. Мы скоро Вам перезвоним."),

    # Mailing
    'success_mailing': _("Теперь вы подписаны на наши предложения.")
}

MESSAGE_TYPE = {
    'callback': 'callback'
}

HOME_TITLE = {
    'olive': _('ДОМ OLIVE'),
    'terra': _('ДОМ TERRA'),
    'obsidian': _('ДОМ OBSIDIAN')
}

SHARE_APART_PAGE = {
    'olive': _('Забронировать дом OLIVE'),
    'terra': _('Забронировать дом TERRA'),
    'obsidian': _('Забронировать дом OBSIDIAN')
}

def set_language(request, language):
    view = None
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            referer_path = urlparse(request.META.get("HTTP_REFERER")).path
            view = resolve(referer_path)
        except Resolver404:
            continue
        break
    
    if view:
        translation.activate(language)
        if hasattr(view, 'url_name'):
            url_name = view.url_name
        else:
            url_name = None

        next_url = reverse(url_name, args=view.args, kwargs=view.kwargs) if url_name else "/"
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response


def indexPage(request):
    current_language = request.LANGUAGE_CODE

    context = {
        'cur_lang': current_language
    }
    return render(request, 'index/index.html', context)


def developPage(request, pageType):
    current_language = request.LANGUAGE_CODE
    description = ''
    if pageType == 'apartments':
        description = _('аренды апартаментов')
    if pageType == 'services':
        description = _('оказываемых услуг')
    if pageType == 'events':
        description = _('проведения мероприятий')

    context = {
        'cur_lang': current_language,
        'description': description
    }
    return render(request, 'index/development.html', context)


def privacyPage(request):
    current_language = request.LANGUAGE_CODE

    context = {
        'cur_lang': current_language,
    }
    return render(request, 'index/privacy.html', context)


def apartmentsPage(request):
    current_language = request.LANGUAGE_CODE

    context = {
        'cur_lang': current_language
    }
    return render(request, 'index/apartments.html', context)


def apartHomePage(request, title):
    current_language = request.LANGUAGE_CODE

    if title in HOME_TITLE:
        apartment = Apartment.objects.get(title=title)
        imageFolderPath = os.path.join(settings.STATIC_ROOT, 'img', 'apartments', title)
        imageFiles = os.listdir(imageFolderPath)
        context = {
            'homeTitle': HOME_TITLE[title],
            'homeGuests': apartment.guests,
            'homeSquare': apartment.square,
            'homeSleep': apartment.sleepPlace,
            'homeWiFi': apartment.isWifi,
            'cur_lang': current_language,
            'imageFolderPath': imageFolderPath,
            'imageFiles': imageFiles,
            'title': title,
            'homeShare': SHARE_APART_PAGE[title]
        }

        return render(request, 'index/apartment-home.html', context)
    else:
        return render(request, 'index/development.html')
    

@csrf_exempt
def orderCall(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        if len(name) > 0 and len(phone) > 0:
            for n in name:
                if n.isdigit():
                    return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_name']})

            for p in phone:
                if p.isalpha():
                    return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})

            belarus_pattern = r'^(?:\+375|375)?\d{9}$'
            russia_pattern = r'^(?:\+7|7)?\d{10}$'

            is_belarus_number = re.match(belarus_pattern, phone)
            is_russian_number = re.match(russia_pattern, phone)

            if is_belarus_number or is_russian_number:
                create_callback.delay(name, phone)
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_callback']}, safe=False)
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})
        else:
            if len(name) == 0:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_name']}, safe=False)
            if len(phone) == 0:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_phone']}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})
    

def sendMail(type, name, phone, created):
    try:
        if type == MESSAGE_TYPE['callback']:
            message = render_to_string('mailing/admin_callback.html', {'name': name, 'phone': phone, 'created': created})
            recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
            send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES["invalid_request"]}, safe=False)
    

def contactsPage(request):
    current_language = request.LANGUAGE_CODE

    context = {
        'cur_lang': current_language
    }
    return render(request, 'index/contacts.html', context)


@csrf_exempt
def saveEmail(request):
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
    

# def rentPage(request):
#     current_language = request.LANGUAGE_CODE

#     context = {
#         'cur_lang': current_language
#     }
#     return render(request, 'index/rent.html', context)


def territoryPage(request):
    current_language = request.LANGUAGE_CODE
    
    folder_path = 'img/territory'
    full_folder_path = os.path.join(settings.STATICFILES_DIRS[0], folder_path)

    image_paths = []
    for filename in os.listdir(full_folder_path):
        img_path = os.path.join(folder_path, filename)
        image_paths.append(img_path)

    context = {
        'cur_lang': current_language,
        "image_paths": image_paths
    }
    return render(request, 'index/territoryGallery.html', context)