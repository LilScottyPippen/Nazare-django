import json
import threading
from datetime import datetime
from django.views import View
from utils.is_valid_name import is_valid_name
from utils.is_valid_phone import is_valid_phone
from utils.send_mail import send_mail_for_admin
from index.forms.callback_form import CallbackForm
from utils.json_responses import error_response, success_response
from utils.constants import ERROR_MESSAGES, MAILING_SUBJECTS, SUCCESS_MESSAGES


class CallbackAPIView(View):
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            client_data = data.get('client_data', {})

            for client_key, client_value in client_data.items():
                if client_key == 'name' and is_valid_name(client_value) is False:
                    return error_response(ERROR_MESSAGES['invalid_name'])
                if client_key == 'phone' and is_valid_phone(client_value) is False:
                    return error_response(ERROR_MESSAGES['invalid_phone'])
                if client_key == 'captcha' and len(str(client_value)) == 0:
                    return error_response(ERROR_MESSAGES['invalid_captcha'])
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