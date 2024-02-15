from django.db import models


class Callback(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    is_privacy_policy = models.BooleanField(default=False, verbose_name='Соглашение о конфиденциальности')
    status = models.BooleanField(default=False, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = "Заявка на звонок"
        verbose_name_plural = "Заявки на звонок"