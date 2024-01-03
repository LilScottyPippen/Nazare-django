from django.contrib import admin
from index.models import *


class AdressInline(admin.TabularInline):
    model = Address
    extra = 1


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1


class TelephonInline(admin.TabularInline):
    model = Telephon
    extra = 1


@admin.register(ContactPage)
class ContactPageView(admin.ModelAdmin):
    inlines = [AdressInline, EmailInline, TelephonInline]
