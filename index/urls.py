from .views import *
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    # PAGES
    path('', IndexPageView.as_view(), name='indexPage'),
    path('development/<str:pageType>', DevelopPageView.as_view(), name='developPage'),
    path('apartments/', ApartmentsPageView.as_view(), name='apartmentsPage'),
    path('apartments/home/<str:title>', ApartHomePageView.as_view(), name='apartHomePage'),
    path('privacy/', PrivacyPageView.as_view(), name='privacyPage'),
    path('contacts/', ContactsPageView.as_view(), name="contactsPage"),
    # path('rent/', rent_page, name='rentPage'),
    path('gallery/territory/', TerritoryPageView.as_view(), name='territoryPage'),

    # FUNCTIONS
    path('order-call/', OrderCallView.as_view(), name='orderCallFunc'),
    path('save-email/', save_email, name='saveEmailFunc')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)