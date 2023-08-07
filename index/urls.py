from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)