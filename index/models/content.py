from django.db import models
from utils.pathes import photo_content_path


class Content(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    img = models.ImageField(upload_to=photo_content_path, verbose_name="Фото")
    description = models.TextField(verbose_name="Описание")
    slug = models.CharField(max_length=255, verbose_name="Псевдоним")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контент"