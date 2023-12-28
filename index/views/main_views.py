from django.views.generic import TemplateView
from index.models import *


class IndexPageView(TemplateView):
    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["houses"] = ApartamentMenu.objects.all()
        return context


class ApartamentPageView(TemplateView):
    template_name = "index/apartament.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apartament = Apartament.objects.get(
            slug=kwargs['apartament'])

        context["apartament"] = apartament
        context["price_lists"] = ApartamentPriceList.objects.filter(
            apartament=apartament)
        context["photos"] = ApartamentPhotoGalery.objects.filter(
            apartament=apartament)
        context["conveniences"] = ApartamentConvenience.objects.filter(
            apartament=apartament)
        context["first_photo"] = context["photos"].first()
        return context
