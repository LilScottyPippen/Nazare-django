from django.contrib import admin
from .models.booking import Booking
from .models.guest import Guest

admin.site.register(Booking)
admin.site.register(Guest)