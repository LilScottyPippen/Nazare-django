import json
import threading
from datetime import datetime
from django.views import View
from django.http import RawPostDataException
from utils.is_valid_name import is_valid_name
from utils.is_valid_phone import is_valid_phone
from utils.send_mail import send_mail_for_admin
from django_ratelimit.decorators import ratelimit
from index.forms.callback_form import CallbackForm
from django.utils.decorators import method_decorator
from utils.is_valid_captcha import is_valid_session_captcha
from utils.json_responses import error_response, success_response
from utils.constants import ERROR_MESSAGES, MAILING_SUBJECTS, SUCCESS_MESSAGES, CAPTCHA_SUBJECT


class CallbackAPIView(View):
    @method_decorator(ratelimit(key='ip', rate='10/m'))
    def post(self, request, **kwargs):
        try:
            try:
                data = json.loads(request.body)
            except RawPostDataException:
                return error_response(ERROR_MESSAGES['bad_request'])

            client_data = data.get('client_data', {})

            if not is_valid_session_captcha(request, CAPTCHA_SUBJECT['callback_captcha']):
                return error_response(ERROR_MESSAGES['invalid_captcha'])

            for client_key, client_value in client_data.items():
                if client_key == 'name' and not is_valid_name(client_value):
                    return error_response(ERROR_MESSAGES['invalid_name'])
                if client_key == 'phone' and not is_valid_phone(client_value):
                    return error_response(ERROR_MESSAGES['invalid_phone'])
        except ValueError:
            return error_response(ERROR_MESSAGES['invalid_form'])

        form = CallbackForm(client_data)

        try:
            callback_context = {
                'name': client_data['name'],
                'phone': client_data['phone'],
                'created': datetime.now()
            }
        except KeyError:
            return error_response(ERROR_MESSAGES['invalid_form'])

        if form.is_valid():
            form.save()
            threading.Thread(target=send_mail_for_admin,
                             args=(MAILING_SUBJECTS['callback_admin'], 'mailing/admin_callback.html', callback_context)).start()
            return success_response(SUCCESS_MESSAGES['success_callback'])
        return error_response(ERROR_MESSAGES['invalid_form'])