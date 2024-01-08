from index.models import ApartmentMenu


def common_context(request):
    return {'houses': ApartmentMenu.objects.all()}
