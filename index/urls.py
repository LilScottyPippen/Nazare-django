from .views import *
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),
    path('apartments/', apartmentsPage, name='apartmentsPage'),
    path('apartments/home/<str:title>', apartHomePage, name='apartHomePage'),
    path('privacy/', privacyPage, name='privacyPage'),
    path("contacts/", contactsPage, name="contactsPage"),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc'),
    path('save-email/', saveEmail, name='saveEmailFunc')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)