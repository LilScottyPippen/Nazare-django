from django.db import models
from django.urls import reverse

from utils.pathes import *


class RedirectPage(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    url_name = models.CharField(max_length=255, verbose_name="Псевдоним ссылки в виде: app:name")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страница для перенаправления"
        verbose_name_plural = "Страницы для перенаправления"


class Category(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Наименование категории")
    slug = models.SlugField(unique=True, primary_key=True, db_index=True,
                            verbose_name="Псеводним для url")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index:category', kwargs={'category': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Подкатегория")
    name = models.CharField(
        max_length=255, verbose_name="Наименование подкатегории")
    image = models.ImageField(
        upload_to=photo_subcategory_path, verbose_name="Изображение подкатегории")
    slug = models.SlugField(verbose_name="Псеводним для url")
    redirect_page = models.ForeignKey(
        RedirectPage, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Перенаправление на страницу")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index:subcategory', kwargs={'category': self.slug})

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
