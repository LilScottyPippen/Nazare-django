from django.views.generic import TemplateView
from index.models import *


class PhotoGalleryCategoryView(TemplateView):
    template_name = "index/gallery/photo_gallery/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = PhotoGalleryCategory.objects.all()
        return context


class PhotoGallerySubCategoryView(TemplateView):
    pass


class PhotoGalleryView(TemplateView):
    template_name = "index/gallery/photo_gallery/photos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = PhotoGalleryCategory.objects.get(slug=kwargs['category'])
        context["photos"] = PhotoGallery.objects.filter(
            photot_gallery_category=category)
        return context
