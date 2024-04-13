from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from index.models import Apartment, Category, SubCategory, PhotoGallery


class StaticSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return ['index:index', 'index:contact', 'index:policy', 'booking:booking']

    def location(self, item):
        return reverse(item)


class ApartmentSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return Apartment.objects.all()


class CategorySitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return Category.objects.all()


class SubCategorySitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return SubCategory.objects.all()