from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_mail_for_admin(message_url, context):
    message = render_to_string(message_url, context)
    recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
    send_mail('', message, settings.EMAIL_HOST_USER, recipient_list)


def send_mail_for_client(client_mail, message_url, context):
    message = render_to_string(message_url, context)
    recipient_list = [client_mail]
    send_mail('', message, settings.EMAIL_HOST_USER, recipient_list)