from django.contrib import admin
from .models.booking import *
from .models.guest import Guest


class GuestInline(admin.TabularInline):
    model = Guest
    extra = 1


baseBookingFields = [
    ('check_in_date', 'check_out_date'),
    ('guests_count', 'children_count'),
    ('client_name', 'client_surname', 'client_father_name',
     'client_mail', 'client_phone'),
    'payment_method',
    ('total_sum', 'is_paid'),
    'comment',
]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'guests_count', 'children_count', 'payment_method', 'is_paid', 'total_sum')

    fields = [
        'apartment',
        *baseBookingFields,
        'confirmed',
        'is_privacy_policy'
    ]

    inlines = [GuestInline]


@admin.register(MultiApartmentBooking)
class MultiApartmentBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_apartments', 'guests_count',
                    'children_count', 'payment_method', 'is_paid', 'total_sum')

    fields = [
        'apartments',
        *baseBookingFields,
    ]

    def display_apartments(self, obj):
        return ", ".join([apartment.title for apartment in obj.apartments.all()])

    display_apartments.short_description = 'Апартаменты'
