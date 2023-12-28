from django.views.generic import TemplateView
from index.models import *


class IndexPageView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = ApartamentMenu.objects.all()
        return context
