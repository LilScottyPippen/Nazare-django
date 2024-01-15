from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = "booking"

urlpatterns = [
    path('booking', BookingView.as_view(), name='booking'),
    path('adding-form', GuestView.as_view(), name='adding_form')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)