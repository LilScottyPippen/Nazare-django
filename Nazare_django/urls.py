from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('root/', admin.site.urls),
    path('', include('index.urls')),
]

if not settings.MAINTENANCE_MODE:
    urlpatterns.append(path('', include('booking.urls')))