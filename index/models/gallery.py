from .category import *


class PhotoGallery(models.Model):
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория фотогалереи")
    photo = models.ImageField(
        upload_to=photo_gallery_path, verbose_name="Фото")
    description = models.CharField(max_length=255, default="Фото", verbose_name="Описание")

    class Meta:
        verbose_name = "Фото для фотогалереи"
