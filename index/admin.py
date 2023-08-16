from django.contrib import admin
from .models import *

@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Обратный звонок'
    list_display = ('id', 'name', 'phone', 'created_at', 'is_answered')

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    verbose_name_plureal = 'Апартаменты'
    list_display = ('id', 'title', 'guests', 'square', 'sleepPlace', 'isWifi')

admin.site.register(ApartmentPhoto)