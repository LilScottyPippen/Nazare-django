from .models import *
from django.contrib import admin


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Обратный звонок'
    list_display = ('id', 'name', 'phone', 'created_at', 'is_answered')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Апартаменты'
    list_display = ('id', 'title', 'guests', 'square', 'sleepPlace', 'dailyPrice')


admin.site.register(Mail)
