from index.models import PhotoGallery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def load_photos(request, subcategory):
    page = request.GET.get("page")
    photos = PhotoGallery.objects.filter(subcategory=subcategory)
    paginator = Paginator(photos, 6)
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return photos
