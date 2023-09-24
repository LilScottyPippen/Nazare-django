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

DEVELOP_DESCRIPTION = {
    'apartments': _('аренды апартаментов'),
    'services': _('оказываемых услуг'),
    'events': _('проведения мероприятий'),
}