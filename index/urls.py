from .views import *
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    # PAGES
    path('', IndexPageView.as_view(), name='indexPage'),
    path('development/<str:pageType>', DevelopPageView.as_view(), name='developPage'),
    path('catalog/<str:pageType>', CatalogPageView.as_view(), name='catalogPage'),
    path('apartments/home/<str:title>', ApartHomePageView.as_view(), name='apartHomePage'),
    path('privacy/', PrivacyPageView.as_view(), name='privacyPage'),
    path('contacts/', ContactsPageView.as_view(), name="contactsPage"),
    path('service/<str:slug>', ServicePageView.as_view(), name='servicePage'),
    path('gallery/<str:category>', GalleryPageView.as_view(), name='galleryPage'),
    # path('rent/', RentPageView.as_view(), name='rentPage'),

    # FUNCTIONS
    path('order-call/', OrderCallView.as_view(), name='orderCallFunc'),
    path('save-email/', SaveEmailView.as_view(), name='saveEmailFunc')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
