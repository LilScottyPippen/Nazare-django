from django.http import Http404
from index.models import SubCategory
from django.views.generic import TemplateView
from utils.load_photos_in_gallery import load_photos


class PhotoGalleryView(TemplateView):
    template_name = "index/gallery/photo_gallery/photos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = kwargs['subcategory']
        context['photos'] = load_photos(self.request, subcategory, 6)
        try:
            context['category'] = SubCategory.objects.filter(
                slug=subcategory
            ).first().name
        except AttributeError:
            raise Http404
        return context


class PhotoGalleryLoadMoreView(TemplateView):
    template_name = "index/gallery/photo_gallery/photo_gallery_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = load_photos(self.request, kwargs['subcategory'], 6)
        return context
