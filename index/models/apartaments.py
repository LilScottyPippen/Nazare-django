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
    slug = models.SlugField(verbose_name="Псевдним для url ссылки")

    def __str__(self):
        return self.title
