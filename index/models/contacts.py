from django.db import models


class ContactPage(models.Model):
    name = models.CharField(
        max_length=255, default="Связывает все поля", verbose_name="Наиенование")

    class Meta:
        verbose_name = "Страница - Контакты"
        verbose_name_plural = "Страница - Контакты"


class Address(models.Model):
    contact = models.ForeignKey(
        ContactPage, on_delete=models.PROTECT, verbose_name="Контактная страница")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адрес"


class Telephon(models.Model):
    contact = models.ForeignKey(
        ContactPage, on_delete=models.PROTECT, verbose_name="Контактная страница")

    number = models.CharField(max_length=255, verbose_name="Телефон")

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефон"


class Email(models.Model):
    contact = models.ForeignKey(
        ContactPage, on_delete=models.PROTECT, verbose_name="Контактная страница")

    email = models.EmailField(verbose_name="E-mail")

    class Meta:
        verbose_name = "E-mail"
