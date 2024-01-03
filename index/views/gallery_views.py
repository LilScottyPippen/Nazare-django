from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from index.models import *


class PhotoGalleryCategoryView(TemplateView):
    template_name = "index/gallery/photo_gallery/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = PhotoGalleryCategory.objects.all()
        return context


class PhotoGallerySubCategoryView(TemplateView):
    template_name = "index/gallery/photo_gallery/subcategory.html"

    def get(self, *args, **kwargs):
        subcategory = PhotoGallerySubCategory.objects.filter(
            category=kwargs['category'])
        if subcategory.count() == 1:
            return HttpResponseRedirect(reverse('index:photo_gallery', args=[subcategory.first().slug]))
        context = self.get_context_data(**kwargs)
        context['subcategories'] = subcategory
        return self.render_to_response(context)


class PhotoGalleryView(TemplateView):
    template_name = "index/gallery/photo_gallery/photos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = PhotoGallery.objects.filter(
            subcategory=kwargs['subcategory'])
        return context
