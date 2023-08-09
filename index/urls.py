from .views import *
from django.conf import settings
from django.views.static import serve
from django.urls import path, re_path

urlpatterns = [
    # PAGES
    path('', indexPage, name='indexPage'),
    path('development/<str:pageType>', developPage, name='developPage'),

    # FUNCTIONS
    path('order-call/', orderCall, name='orderCallFunc')
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]