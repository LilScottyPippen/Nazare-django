from .views import *
from django.urls import path



urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
]