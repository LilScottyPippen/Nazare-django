import requests
from Nazare_django import settings


def is_valid_captcha(response):
    result = requests.post(
        settings.RECAPTCHA_API_URL,
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': response,
        }, verify=True
    ).json().get("success", False)
    return result


def is_valid_session_captcha(request, subject):
    session_captcha = request.session.get(f'{subject}_captcha')
    return session_captcha is True
