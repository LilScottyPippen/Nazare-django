from django.urls import path
from .views import BookingView
from Nazare_django import settings
from django.conf.urls.static import static

app_name = "booking"

urlpatterns = [
    path('booking', BookingView.as_view(), name='booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)