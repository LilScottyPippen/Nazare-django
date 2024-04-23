from django.views import View
from index.models import Subscriber
from index.forms.subscriber_form import SubscriberForm
from utils.is_valid_captcha import is_valid_session_captcha
from utils.json_responses import error_response, success_response
from utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES, CAPTCHA_SUBJECT


class SubscriberAPIView(View):
    def post(self, request, **kwargs):
        client_mail = request.POST.get('mail')

        if not client_mail:
            return error_response(ERROR_MESSAGES['invalid_form'])

        if is_valid_session_captcha(request, CAPTCHA_SUBJECT['subscribe_captcha']):
            try:
                del request.session[f'{CAPTCHA_SUBJECT["subscribe_captcha"]}_captcha']
            except KeyError:
                return error_response(ERROR_MESSAGES['invalid_captcha'])
        else:
            return error_response(ERROR_MESSAGES['invalid_captcha'])

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return success_response(SUCCESS_MESSAGES['success_subscribed'])
        else:
            if Subscriber.objects.filter(mail=client_mail):
                return error_response(ERROR_MESSAGES['duplicate_mail'])
            return error_response(ERROR_MESSAGES['invalid_form'])
