from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from index.views import set_language
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),

    path('set_language/<str:language>', set_language, name='set_language')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
