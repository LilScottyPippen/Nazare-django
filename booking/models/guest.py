from django.db import models
from ..models.booking import *


class Guest(models.Model):
    NATION_CHOICES = [
        ("RU", "Россия"),
        ("BY", "Беларусь"),
    ]

    guest_name = models.CharField(max_length=50)
    guest_second_name = models.CharField(max_length=50)
    guest_father_name = models.CharField(max_length=50)
    citizenship = models.CharField(max_length=2, choices=NATION_CHOICES)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
