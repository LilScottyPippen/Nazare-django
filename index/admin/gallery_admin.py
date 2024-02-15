from django.contrib import admin
from index.models import *


class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    extra = 1
    fields = ('photo', 'description')
