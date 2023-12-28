from django.db import models

PAYMENT_METHOD_CHOICES = [
    ("ON", "Online"),
    ("OF", "Offline")
]


class Booking(models.Model):
    apartment_id = models.IntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_count = models.IntegerField()
    children_count = models.IntegerField()
    client_name = models.CharField(max_length=50)
    client_surname = models.CharField(max_length=50)
    client_father_name = models.CharField(max_length=50)
    client_email = models.EmailField()
    client_number = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    total_sum = models.FloatField()
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES[0])

    def __str__(self):
        return str(self.id)