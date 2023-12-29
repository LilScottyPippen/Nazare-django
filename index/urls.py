from django.urls import path
from index.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "index"

urlpatterns = [
    path('', IndexPageView.as_view(), name="index"),
    path('apartaments/<slug:apartament>',
         ApartamentPageView.as_view(), name="apartament"),
    path('photo_gallery/', PhotoGalleryCategoryView.as_view(), name="photo_gallery"),
    path('photo_gallery/<slug:category>',
         PhotoGalleryView.as_view(), name="photos"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
