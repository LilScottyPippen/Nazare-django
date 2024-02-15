from django.db import models
from utils.pathes import apartment_photo_path


class Apartment(models.Model):
    title = models.CharField(unique=True, max_length=20,
                             verbose_name="Наименование апартамента")
    guest_count = models.PositiveSmallIntegerField(
        verbose_name="Кол-во гостей")
    square = models.FloatField(verbose_name="Площадь")
    sleep_place_count = models.PositiveSmallIntegerField(
        verbose_name="Кол-во спальных мест")
    daily_price = models.FloatField(
        default=0.0, verbose_name="Суточная стоимость (BYN)")
    room_count = models.PositiveSmallIntegerField(
        verbose_name="Количество комнат")

    slug = models.SlugField(verbose_name="Псевдоним для url ссылки")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Наполнение страницы с апартаментом"
        verbose_name_plural = "Наполнение страницы с апартаментами"


class ApartmentPriceList(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.PROTECT, verbose_name="Апартамент")
    name = models.CharField(max_length=255, verbose_name="Наименование услуги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "В стоимость входит"
        verbose_name_plural = "В стоимость входят"


class ApartmentConvenience(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.PROTECT, verbose_name="Апартамент")
    name = models.CharField(max_length=255, verbose_name="Наименование удобства")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"


class ApartmentPhotoGallery(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.PROTECT, verbose_name="Апартамент")
    photo = models.ImageField(
        upload_to=apartment_photo_path, verbose_name="Фото")
    description = models.CharField(max_length=255, default="Фото", verbose_name="Описание")


class ApartmentMenu(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.PROTECT, verbose_name="Апартамент")
    apartment_description = models.TextField(
        verbose_name="Описание апартамента")
    apartment_main_photo = models.ImageField(verbose_name="Главное фото")

    class Meta:
        verbose_name = "Наполнение для главной страницы"
        verbose_name_plural = "Наполнения для главной страницы"
