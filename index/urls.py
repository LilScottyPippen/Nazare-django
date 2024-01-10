from django.urls import path
from index.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "index"

urlpatterns = [
    path('', IndexPageView.as_view(), name="index"),
    path('apartments/<slug:apartment>',
         ApartmentPageView.as_view(), name="apartment"),
    path('category/<slug:category>',
         CategoryView.as_view(), name="category"),
    path('subcategory/<slug:category>',
         SubCategoryView.as_view(), name="subcategory"),
    path('photo-gallery/<slug:subcategory>',
         PhotoGalleryView.as_view(), name="photo_gallery"),
    path('photo-gallery/load-more/<slug:subcategory>',
         PhotoGalleryLoadMoreView.as_view(), name="photo_gallery_load_more"),
    path('contact/', ContactPageView.as_view(), name="contact")

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
