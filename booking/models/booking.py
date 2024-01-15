from django.db import models

PAYMENT_METHOD_CHOICES = [
    ("ON", "Online"),
    ("OF", "Offline")
]


class Booking(models.Model):
    apartment = models.IntegerField(verbose_name='Апартамент')
    check_in_date = models.DateField(verbose_name='Дата заезда')
    check_out_date = models.DateField(verbose_name='Дата выезда')
    guests_count = models.IntegerField(verbose_name='Количество гостей')
    children_count = models.IntegerField(verbose_name='Количество детей')
    client_name = models.CharField(max_length=50, verbose_name='Имя')
    client_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    client_father_name = models.CharField(max_length=50, verbose_name='Отчество')
    client_mail = models.EmailField(verbose_name='Электронная почта')
    client_phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    total_sum = models.FloatField(verbose_name='Сумма')
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES[0],
                                      verbose_name='Способ оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"