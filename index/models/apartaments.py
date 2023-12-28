from django.db import models


class Apartament(models.Model):
    title = models.CharField(unique=True, max_length=20,
                             verbose_name="Наименование апартоментов")
    guest_count = models.PositiveSmallIntegerField(
        verbose_name="Кол-во гостей")
    square = models.FloatField(verbose_name="Площадь")
    sleep_place_count = models.PositiveSmallIntegerField(
        verbose_name="Кол-во спальных мест")
    daily_price = models.FloatField(
        default=0.0, verbose_name="Суточная стоимость (BYN)")
    room_count = models.PositiveSmallIntegerField(
        verbose_name="Количество комнат")

    slug = models.SlugField(verbose_name="Псевдним для url ссылки")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Наполнение страницы с апартаментами"
        verbose_name_plural = "Наполнение страницы с апартаментами"


class ApartamentPriceList(models.Model):
    apartament = models.ForeignKey(
        Apartament, on_delete=models.PROTECT, verbose_name="Апартаменты")
    name = models.CharField(max_length=255, verbose_name="Наименование услуги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "В стоимость входит"
        verbose_name_plural = "В стоимость входит"


class ApartamentConvenience(models.Model):
    apartament = models.ForeignKey(
        Apartament, on_delete=models.PROTECT, verbose_name="Апартаменты")
    name = models.CharField(max_length=255, verbose_name="Удобства")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Удобства"
        verbose_name_plural = "Удобства"


def apartament_photo_path(instance, file_name):
    return f"apartaments/{instance.apartament.title}/{file_name}"


class ApartamentPhotoGalery(models.Model):
    apartament = models.ForeignKey(
        Apartament, on_delete=models.PROTECT, verbose_name="Апартаменты")
    photo = models.ImageField(
        upload_to=apartament_photo_path, verbose_name="Фото")


class ApartamentMenu(models.Model):
    apartament = models.ForeignKey(
        Apartament, on_delete=models.PROTECT, verbose_name="Апартаменты")
    apartament_description = models.TextField(
        verbose_name="Описание апартаментов")
    apartament_main_photo = models.ImageField(verbose_name="Главное фото")

    class Meta:
        verbose_name = "Наполнение для главной страницы"
        verbose_name_plural = "Наполнение для главной страницы"
