from .views import *
from django.urls import path



urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),
    path('apartments/home/<int:num>', apartHomePage, name='apartHomePage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
]