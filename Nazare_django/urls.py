from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('root/', admin.site.urls),
    path('', include('index.urls')),
]

if not settings.MAINTENANCE_MODE:
    urlpatterns.append(path('', include('booking.urls')))
    urlpatterns.append(path('api/', include('api.urls')))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)