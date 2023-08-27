from .constants import *
from django.conf import settings
from .models import Callback, Mail
from ZorkaDjango.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string


from celery import shared_task

@app.task
def create_callback(callback_id):
    try:
        callback = Callback.objects.get(id=callback_id)
        message = render_to_string('mailing/admin_callback.html', {'name': callback.name, 'phone': callback.phone, 'created': callback.created_at})
        recipient_list = ['lilscottypippen33@gmail.com']
        send_mail(MESSAGE_TYPE['callback'], message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        return True
    except Exception as e:
        print(e)