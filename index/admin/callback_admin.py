from ..models.callback import *
from django.contrib import admin


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status')

    fields = ('name', 'phone', 'status')