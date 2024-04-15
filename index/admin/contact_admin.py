from index.models import *
from django.contrib import admin


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


@admin.register(ContactPage)
class ContactPageView(admin.ModelAdmin):
    inlines = [AddressInline, EmailInline, PhoneInline]
