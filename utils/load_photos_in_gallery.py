from index.models import PhotoGallery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from index.models.category import SubCategory
from django.shortcuts import get_object_or_404


def load_photos(request, subcategory, count):
    page = request.GET.get("page")
    subcategory_obj = get_object_or_404(SubCategory, slug=subcategory)
    photos_queryset = PhotoGallery.objects.filter(subcategory=subcategory_obj).order_by('id')
    paginator = Paginator(photos_queryset, count)
    try:
        photos_page = paginator.page(page)
    except PageNotAnInteger:
        photos_page = paginator.page(1)
    except EmptyPage:
        photos_page = paginator.page(paginator.num_pages)
    return photos_page

