from django.urls import path
from .views import *

urlpatterns = [
    path('booking', BookingView.as_view(), name='booking'),
    path('adding-form', GuestView.as_view(), name='adding_form')
]