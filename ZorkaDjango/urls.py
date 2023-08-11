from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from index.views import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),

    path('set_language/<str:language>', set_language, name='set_language')
]