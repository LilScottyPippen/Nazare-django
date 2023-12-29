from django.contrib import admin
from index.models import *


class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    extra = 1
    fields = ('photo',)


class PhotoGallerySubCategoryInline(admin.StackedInline):
    model = PhotoGallerySubCategory
    extra = 1


@admin.register(PhotoGalleryCategory)
class PhotoGalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

    inlines = [PhotoGallerySubCategoryInline]


@admin.register(PhotoGallerySubCategory)
class PhotoGallerySubCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name')

    inlines = [PhotoGalleryInline]
