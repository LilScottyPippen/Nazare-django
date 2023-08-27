# В tests.py
from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from .models import Callback
from .tasks import *
from .constants import MESSAGE_TYPE
from unittest.mock import patch, call

class CallbackTestCase(TestCase):
    def test_create_callback(self):
        create_callback(Callback.objects.create(name="Denis", phone="321321321").id)
