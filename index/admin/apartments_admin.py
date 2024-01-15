from django.contrib import admin
from index.models import *

# Register your models here.


class ApartmentMenuInline(admin.StackedInline):
    model = ApartmentMenu
    extra = 1
    max_num = 1


class ApartmentPriceListInline(admin.TabularInline):
    model = ApartmentPriceList
    extra = 1


class ApartmentConvenienceInline(admin.TabularInline):
    model = ApartmentConvenience
    extra = 1


class ApartmentPhotoInline(admin.TabularInline):
    model = ApartmentPhotoGallery
    extra = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'guest_count',
                    'square', 'daily_price', 'slug')
    list_editable = ('title', 'guest_count', 'square', 'slug')

    fields = [('title', 'slug'), ('guest_count',
                                  'square', 'room_count', 'sleep_place_count'), 'daily_price']

    inlines = [ApartmentMenuInline, ApartmentPriceListInline,
               ApartmentConvenienceInline, ApartmentPhotoInline]
