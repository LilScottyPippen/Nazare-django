from django.contrib import admin
from .models.booking import Booking
from .models.guest import Guest


class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'guests_count', 'children_count', 'payment_method', 'is_paid', 'total_sum')

    inlines = [GuestInline]
