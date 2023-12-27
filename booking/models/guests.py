from django.db import models


class Guests(models.Model):
    NATION_CHOICES = {
        "RU": "Русский",
        "RB": "Беларус"
    }
    guest_name = models.CharField(max_length=50)
    guest_second_name = models.CharField(max_length=50)
    guest_father_name = models.CharField(max_length=50)
    nationality = models.CharField(choices=NATION_CHOICES)
