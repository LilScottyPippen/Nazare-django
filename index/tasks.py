from django.utils import timezone
from django.conf import settings
from .models import Callback
from django.core.mail import send_mail
from django.template.loader import render_to_string
from ZorkaDjango.celery import app
from django.http import JsonResponse
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


@app.task
def create_callback(name, phone):
    try:
        callback = Callback.objects.create(name=name, phone=phone)
    except Exception as e:
        if 'callback' in locals():
            callback.delete()
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})
    sendMail(MESSAGE_TYPE['callback'], name, phone, callback.created_at)


def sendMail(type, name, phone, created):
    try:
        if type == MESSAGE_TYPE['callback']:
            message = render_to_string('mailing/admin_callback.html', {'name': name, 'phone': phone, 'created': created})
            recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
            send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    except:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES["invalid_request"]}, safe=False)