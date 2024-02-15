from django.db import models


class Subscriber(models.Model):
    mail = models.EmailField(unique=True, verbose_name="Электронная почта")

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = "Подписчик на рассылку"
        verbose_name_plural = "Подписчики на рассылку"


class Mailing(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"