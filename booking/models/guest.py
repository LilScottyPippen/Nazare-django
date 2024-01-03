from django.db import models
from ..models.booking import *

CITIZENSHIP_CHOICES = [
    ("RU", "Россия"),
    ("BY", "Беларусь"),
]


class Guest(models.Model):
    guest_name = models.CharField(max_length=50, verbose_name='Имя')
    guest_second_name = models.CharField(max_length=50, verbose_name='Фамилия')
    guest_father_name = models.CharField(max_length=50, verbose_name='Отчество')
    citizenship = models.CharField(max_length=2, choices=CITIZENSHIP_CHOICES, verbose_name='Гражданство')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Бронирование')

    def __str__(self):
        return f'{self.guest_second_name.title()} {self.guest_name.title()[0]}. {self.guest_father_name.title()[0]}.'

    class Meta:
        verbose_name = "Категория гостей"
        verbose_name_plural = "Категории гостей"