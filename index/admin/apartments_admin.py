from django.contrib import admin
from index.models import *


class ApartmentMenuInline(admin.StackedInline):
    model = ApartmentMenu
    extra = 1
    max_num = 1


class ApartmentPhotoInline(admin.TabularInline):
    model = ApartmentPhotoGallery
    extra = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'guest_count',
                    'square', 'daily_price', 'slug')
    list_editable = ('title', 'guest_count', 'square', 'slug')

    fields = [('title', 'slug'), ('guest_count',
                                  'square', 'room_count', 'sleep_place_count'), 'daily_price',
                                  ('convenience_package', 'includedService_package')]

    inlines = [ApartmentMenuInline, ApartmentPhotoInline]


admin.site.register(ConveniencePackage)
admin.site.register(ApartmentConvenience)
admin.site.register(IncludedServicePackage)
admin.site.register(ApartmentIncludedService)