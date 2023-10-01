from .models import *
from django.contrib import admin


@admin.register(Callback)
class CallbackAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Обратный звонок'
    list_display = ('name', 'phone', 'created_at', 'is_answered')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Апартаменты'
    list_display = ('title', 'guests', 'square', 'sleepPlace', 'dailyPrice')


admin.site.register(Mail)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'hourlyPrice')

admin.site.register(Category)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'page_slug')


admin.site.register(PageSlug)