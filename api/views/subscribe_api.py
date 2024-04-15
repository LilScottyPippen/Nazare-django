from django.views import View
from index.models import Subscriber
from index.forms.subscriber_form import SubscriberForm
from utils.constants import ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.json_responses import error_response, success_response


class SubscriberAPIView(View):
    def post(self, request, **kwargs):
        client_mail = request.POST.get('mail')
        captcha_response = request.POST.get('captcha')

        try:
            if len(captcha_response) == 0:
                return error_response(ERROR_MESSAGES['invalid_captcha'])
        except TypeError:
            return error_response(ERROR_MESSAGES['invalid_form'])

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return success_response(SUCCESS_MESSAGES['success_subscribed'])
        else:
            if Subscriber.objects.filter(mail=client_mail):
                return error_response(ERROR_MESSAGES['duplicate_mail'])
            return error_response(ERROR_MESSAGES['invalid_form'])
