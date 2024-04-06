from index.models import ApartmentMenu
import os


def common_context(request):
    return {
        'houses': ApartmentMenu.objects.all(),
        'recaptcha_public_key': os.getenv('RECAPTCHA_PUBLIC_KEY'),
        'check_in_time': os.environ.get('CHECK_IN_TIME', '14:00')
    }
