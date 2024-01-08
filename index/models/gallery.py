from django.db import models
from utils.pathes import *


class PhotoGalleryCategory(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Наименование категории")
    image = models.ImageField(
        upload_to=photo_category_path, default='index/static/img/backgrounds/background-image.jpg', verbose_name="Изображение категории")
    slug = models.SlugField(unique=True, primary_key=True, db_index=True,
                            verbose_name="Псеводним для url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория фотогалереи"
        verbose_name_plural = "Категории фотогалереи"


class PhotoGallerySubCategory(models.Model):
    category = models.ForeignKey(
        PhotoGalleryCategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    name = models.CharField(
        max_length=255, verbose_name="Наименование подкатегории")
    image = models.ImageField(
        upload_to=photo_subcategory_path, default='index/static/img/backgrounds/background-image.jpg', verbose_name="Изображение подкатегории")
    slug = models.SlugField(unique=True, primary_key=True, db_index=True,
                            verbose_name="Псеводним для url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегории для фотогалереи"
        verbose_name_plural = "Подкатегории для фотогалереи"


class PhotoGallery(models.Model):
    subcategory = models.ForeignKey(
        PhotoGallerySubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория фотогалереи",)
    photo = models.ImageField(
        upload_to=photo_gallery_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото для фотогалереи"
