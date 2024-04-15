from index.models import *
from django.contrib import admin


class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    extra = 1
    fields = ('photo', 'description')
