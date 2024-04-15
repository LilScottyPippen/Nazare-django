from django.views import View
from index.models import Subscriber
from utils.is_valid_captcha import is_valid_captcha
from index.forms.subscriber_form import SubscriberForm
from utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.json_responses import error_response, success_response


class SubscriberAPIView(View):
    def post(self, request, **kwargs):
        client_mail = request.POST.get('mail')
        captcha_response = request.POST.get('captcha')

        if not client_mail or not captcha_response:
            return error_response(ERROR_MESSAGES['invalid_form'])

        captcha_result = is_valid_captcha(captcha_response)

        if not captcha_result:
            return error_response(ERROR_MESSAGES['invalid_captcha'])

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return success_response(SUCCESS_MESSAGES['success_subscribed'])
        else:
            if Subscriber.objects.filter(mail=client_mail):
                return error_response(ERROR_MESSAGES['duplicate_mail'])
            return error_response(ERROR_MESSAGES['invalid_form'])
