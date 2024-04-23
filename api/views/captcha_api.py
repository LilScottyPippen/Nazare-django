from django.http import JsonResponse
from django.views import View
from utils.is_valid_captcha import is_valid_captcha


class CaptchaAPI(View):
    def get(self, request, subject, value):
        result = is_valid_captcha(value)
        request.session[f'{subject}_captcha'] = result
        return JsonResponse(result, safe=False, status=200)
