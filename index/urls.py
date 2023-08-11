from .views import *
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),
    path('apartments/home/<int:num>', apartHomePage, name='apartHomePage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)