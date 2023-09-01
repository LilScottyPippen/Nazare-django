from .tasks import *
from django.test import TestCase

class CallbackTestCase(TestCase):
    def test_create_callback(self):
        create_callback(Callback.objects.create(name="Denis", phone="321321321").id)
