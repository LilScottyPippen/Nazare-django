from django.db import models


class Guests(models.Model):
    guest_name = models.CharField(max_length=50)
    guest_second_name = models.CharField(max_length=50)
