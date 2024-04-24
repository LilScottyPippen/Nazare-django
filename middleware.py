from utils.json_responses import error_response
from utils.constants import ERROR_MESSAGES


class RatelimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        from django_ratelimit.exceptions import Ratelimited
        if isinstance(exception, Ratelimited):
            return error_response(ERROR_MESSAGES['too_many_requests'], 429)