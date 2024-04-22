import random
import threading
from datetime import datetime
from django.views import View
from django.utils import timezone
from utils.send_mail import send_mail_for_client
from utils.json_responses import error_response, success_response
from utils.constants import ERROR_MESSAGES, MAILING_SUBJECTS, SUCCESS_MESSAGES, RESET_CODE_TIMEOUT


class SendConfirmationCodeAPIView(View):
    def get(self, request, mail):
        last_request_time_str = request.session.get('last_confirmation_code_request_time')
        if last_request_time_str:
            last_request_time = datetime.strptime(last_request_time_str, "%Y-%m-%d %H:%M:%S.%f")
            if (timezone.now() - last_request_time).seconds < RESET_CODE_TIMEOUT:
                return error_response(ERROR_MESSAGES['code_request_too_soon'])

        confirmation_code = ''.join(str(random.randint(0, 9)) for _ in range(6))

        try:
            request.session['confirmation_code'] = confirmation_code
            request.session['last_confirmation_code_request_time'] = str(timezone.now())
        except Exception as e:
            return error_response(ERROR_MESSAGES['invalid_send_code'])

        threading.Thread(target=send_mail_for_client,
                         args=(MAILING_SUBJECTS['confirm_email'], mail, 'mailing/confirmation_code.html',
                               {'code': confirmation_code})).start()

        return success_response(SUCCESS_MESSAGES['success_send_code'])


class ConfirmEmailAPIView(View):
    def get(self, request, confirmation_code):
        saved_confirmation_code = request.session.get('confirmation_code')
        if saved_confirmation_code == confirmation_code:
            del request.session['confirmation_code']
            return success_response(SUCCESS_MESSAGES['success'])
        else:
            return error_response(ERROR_MESSAGES['incorrect_code'])