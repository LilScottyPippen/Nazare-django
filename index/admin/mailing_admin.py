import threading
from index.models import *
from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives


admin.site.register(Subscriber)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        threading.Thread(target=lambda: self.send_message(obj)).start()
        super().save_model(request, obj, form, change)

    def send_message(self, obj):
        recipient_list = Subscriber.objects.all()
        message = EmailMultiAlternatives(obj.title, obj.content, settings.EMAIL_HOST_USER, [], recipient_list)
        message.send()

