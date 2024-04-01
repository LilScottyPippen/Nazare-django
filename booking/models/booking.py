from django.core.exceptions import ValidationError
from django.db import models
from index.models import Apartment
from utils.constants import ERROR_MESSAGES
from utils.is_valid_date import is_valid_date_booking
from utils.is_valid_phone import is_valid_phone

PAYMENT_METHOD_CHOICES = [
    ("ON", "Online"),
    ("OF", "Offline")
]


class BaseBooking(models.Model):
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')
    guests_count = models.IntegerField(verbose_name='Количество гостей')
    children_count = models.IntegerField(verbose_name='Количество детей')
    client_father_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    total_sum = models.FloatField(verbose_name='Сумма')
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES[0],
                                      verbose_name='Способ оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    def clean(self):
        if not self.pk:
            if not is_valid_date_booking(self.check_in_date, self.check_out_date):
                raise ValidationError({'check_in_date': ERROR_MESSAGES['unavailable_period'],
                                       'check_out_date': ERROR_MESSAGES['unavailable_period']})

    class Meta:
        abstract = True


class Booking(BaseBooking):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Апартамент')
    client_name = models.CharField(max_length=50, verbose_name='Имя')
    client_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    client_mail = models.EmailField(verbose_name='Электронная почта')
    client_phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    is_privacy_policy = models.BooleanField(default=False, verbose_name='Соглашение о конфиденциальности')

    def clean(self):
        super().clean()
        if not is_valid_phone(self.client_phone):
            raise ValidationError({'client_phone': ERROR_MESSAGES['invalid_phone']})

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class MultiApartmentBooking(BaseBooking):
    apartments = models.ManyToManyField(Apartment, verbose_name='Апартаменты')
    client_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    client_surname = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    client_mail = models.EmailField(null=True, blank=True, verbose_name='Электронная почта')
    client_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = "Массовое бронирование"
        verbose_name_plural = "Массовые бронирования"