from django.views import View
from django.conf import settings
from urllib.parse import urlparse
from django.utils import translation
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404


class SetLanguageView(View):
    def get(self, request, language):
        referer = request.META.get("HTTP_REFERER", "/")
        referer_path = urlparse(referer).path
        try:
            view = resolve(referer_path)
        except Resolver404:
            view = None

        if view:
            translation.activate(language)
            url_name = getattr(view, 'url_name', None)
            args = getattr(view, 'args', [])
            kwargs = getattr(view, 'kwargs', {})
            next_url = reverse(url_name, args=args, kwargs=kwargs) if url_name else referer_path
        else:
            next_url = referer_path[len(language) + 1:]
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
