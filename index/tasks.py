from .constants import *
from .models import Callback
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string


@shared_task
def create_callback(callback_id):
    try:
        callback = Callback.objects.get(id=callback_id)
        message = render_to_string('mailing/admin_callback.html',
                                   {'name': callback.name, 'phone': callback.phone, 'created': callback.created_at})
        recipient_list = [admin.email for admin in User.objects.filter(is_superuser=True)]
        send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        return True
    except Exception as e:
        return False
