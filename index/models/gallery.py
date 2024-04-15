from django.db import models
from django.urls import reverse
from .category import SubCategory
from utils.pathes import photo_gallery_path


class PhotoGallery(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория фотогалереи")
    photo = models.ImageField(
        upload_to=photo_gallery_path, verbose_name="Фото")
    description = models.CharField(max_length=255, default="Фото", verbose_name="Описание")

    def __str__(self):
        return self.photo.name

    def get_absolute_url(self):
        return reverse('index:photo_gallery', kwargs={'subcategory': self.subcategory.slug})

    class Meta:
        verbose_name = "Фото для фотогалереи"
