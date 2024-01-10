from django.contrib import admin
from index.models import *
from .gallery_admin import PhotoGalleryInline


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 1
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name')

    inlines = [PhotoGalleryInline]


admin.site.register(RedirectPage)