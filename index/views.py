import re
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
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

ERROR_MESSAGES = {
    'invalid_request': _('Недействительный запрос! Попробуйте еще раз.'),

    # CALLBACK
    'empty_name': _("Поле 'Ваше имя': пустое!"),
    'empty_phone': _("Поле 'Телефон': пустое!"),
    'invalid_name': _('Введите корректное имя!'),
    'invalid_phone': _('Введите корректный номер!')
}

SUCCESS_MESSAGES = {
    # CALLBACK
    'success_callback': _("Спасибо за Вашу заявку. Мы скоро Вам перезвоним.")
}

MESSAGE_TYPE = {
    'callback': 'callback'
}

HOME_TITLE = {
    'olive': _('ДОМ OLIVE'),
    'terra': _('ДОМ TERRA'),
    'obsidian': _('ДОМ OBSIDIAN')
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


def apartHomePage(request, title):
    current_language = request.LANGUAGE_CODE

    if title in HOME_TITLE:
        apartment = Apartment.objects.get(title=title)
        context = {
            'homeTitle': HOME_TITLE[title],
            'homeGuests': apartment.guests,
            'homeSquare': apartment.square,
            'homeSleep': apartment.sleepPlace,
            'homeWiFi': apartment.isWifi,
            'cur_lang': current_language
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
                callback = Callback.objects.create(name=name, phone=phone)
                sendMail(MESSAGE_TYPE['callback'], name, phone, callback.created_at)
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['success_callback']}, safe=False)
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_phone']})
        else:
            if len(name) == 0:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_name']}, safe=False)
            if len(phone) == 0:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['empty_phone']}, safe=False)
    except Exception as e:
        if 'callback' in locals():
            callback.delete()
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})
    

def sendMail(type, name, phone, created):
    try:
        if type == MESSAGE_TYPE['callback']:
            message = render_to_string('mailing/admin_callback.html', {'name': name, 'phone': phone, 'created': created})
            print(message)
            recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
            send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    except:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES["invalid_request"]}, safe=False)