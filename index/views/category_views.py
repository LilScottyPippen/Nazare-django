from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from index.models import *


class CategoryView(TemplateView):
    template_name = "index/category/category.html"

    def get(self, *args, **kwargs):
        subcategory = SubCategory.objects.filter(
            category=Category.objects.get(slug=kwargs['category'])
        )
        context = self.get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=kwargs['category'])
        context['subcategories'] = subcategory
        return self.render_to_response(context)


class SubCategoryView(TemplateView):
    template_name = "index/category/category.html"

    def get(self, *args, **kwargs):
        subcategory = SubCategory.objects.filter(
            category=kwargs['category'])
        if subcategory.count() == 1:
            return HttpResponseRedirect(reverse('index:photo_gallery', args=[subcategory.first().slug]))
        context = self.get_context_data(**kwargs)
        context['subcategories'] = subcategory
        return self.render_to_response(context)
