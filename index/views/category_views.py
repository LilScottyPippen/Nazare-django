from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from index.models import Category, SubCategory
from django.core.exceptions import ObjectDoesNotExist


class CategoryView(TemplateView):
    template_name = "index/category/category.html"

    def get(self, *args, **kwargs):
        try:
            subcategory = SubCategory.objects.filter(
                category=Category.objects.get(slug=kwargs['category'])
            )
        except ObjectDoesNotExist:
            raise Http404
        context = self.get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=kwargs['category'])
        context['subcategories'] = subcategory
        return self.render_to_response(context)


class SubCategoryView(TemplateView):
    template_name = "index/category/category.html"

    def get(self, *args, **kwargs):
        try:
            subcategory = SubCategory.objects.get(category=kwargs['category'])
        except ObjectDoesNotExist:
            raise Http404
        if subcategory.count() == 1:
            return HttpResponseRedirect(reverse('index:photo_gallery', args=[subcategory.first().slug]))
        context = self.get_context_data(**kwargs)
        context['subcategories'] = subcategory
        return self.render_to_response(context)
