from django.contrib import admin
from index.models import *

# Register your models here.


class ApartamentMenuInline(admin.StackedInline):
    model = ApartamentMenu
    extra = 1
    max_num = 1


class ApartamentPriceListInline(admin.TabularInline):
    model = ApartamentPriceList
    extra = 1


class ApartamentConvenienceInline(admin.TabularInline):
    model = ApartamentConvenience
    extra = 1


class ApartamentPhotoInline(admin.TabularInline):
    model = ApartamentPhotoGalery
    extra = 1


@admin.register(Apartament)
class ApartamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'guest_count',
                    'square', 'daily_price', 'slug')
    list_editable = ('title', 'guest_count', 'square', 'slug')

    fields = [('title', 'slug'), ('guest_count',
                                  'square', 'room_count'), 'daily_price']

    inlines = [ApartamentMenuInline, ApartamentPriceListInline,
               ApartamentConvenienceInline, ApartamentPhotoInline]
