from django.urls import path
from index.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "index"

urlpatterns = [
    path('', IndexPageView.as_view(), name="index"),
    path('apartments/<slug:apartment>',
         ApartmentPageView.as_view(), name="apartment"),
    path('apartments/<str:check_in_date>/<str:check_out_date>/<int:guest_count>/<int:children_count>',
         ApartmentSearchView.as_view(), name="apartment_search"),
    path('category/<slug:category>',
         CategoryView.as_view(), name="category"),
    path('subcategory/<slug:category>',
         SubCategoryView.as_view(), name="subcategory"),
    path('photo-gallery/<slug:subcategory>',
         PhotoGalleryView.as_view(), name="photo_gallery"),
    path('photo-gallery/load-more/<slug:subcategory>',
         PhotoGalleryLoadMoreView.as_view(), name="photo_gallery_load_more"),
    path('contact/', ContactPageView.as_view(), name="contact"),
    path('subscribe/', SubscriberView.as_view(), name="subscribe"),
    path('callback/', CallbackView.as_view(), name="callback"),
    path('content/<str:slug>', ContentView.as_view(), name="content")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
