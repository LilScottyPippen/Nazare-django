from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
]