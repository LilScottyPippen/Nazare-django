from django.db import models
from utils.pathes import photo_gallery_path


class PhotoGalleryCategory(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Наименование категории")
    icon = models.CharField(max_length=255, verbose_name="Иконка категории")
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
    icon = models.CharField(max_length=255, verbose_name="Иконка подкатегории")
    slug = models.SlugField(unique=True, primary_key=True, db_index=True,
                            verbose_name="Псеводним для url")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегории для фотогалереи"
        verbose_name_plural = "Подкатегории для фотогалереи"


class PhotoGallery(models.Model):
    subcategory = models.ForeignKey(
        PhotoGallerySubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория Фотогаллереи",)
    photo = models.ImageField(
        upload_to=photo_gallery_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото для фотогалереи"
