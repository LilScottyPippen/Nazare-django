from django.db import models

class Callback(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_answered = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = "Обратный звонок"
        verbose_name_plural = "Обратные звонки"

    def __str__(self):
        return self.phone
    

class Apartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name='Название')
    guests = models.IntegerField(verbose_name='Кол-во гостей')
    square = models.FloatField(verbose_name='Площадь')
    sleepPlace = models.IntegerField(verbose_name='Кол-во спальных мест')
    isWifi = models.BooleanField(verbose_name='Wi-Fi')

    class Meta:
        verbose_name = "Апартаменты"
        verbose_name_plural = "Апартаменты"

    def __str__(self):
        return self.title
