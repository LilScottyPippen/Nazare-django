from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from Nazare_django.sitemaps import *

sitemaps = {
    'static': StaticSitemap,
    'apartment': ApartmentSitemap,
    'category': CategorySitemap,
    'subcategory': SubCategorySitemap,
}

urlpatterns = [
    path('root/', admin.site.urls),
    path('', include('index.urls')),
    path("robots.txt",
         TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
         ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap",
         )
]

if not settings.MAINTENANCE_MODE:
    urlpatterns.append(path('', include('booking.urls')))
    urlpatterns.append(path('api/', include('api.urls')))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
