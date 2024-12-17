from django.contrib.sitemaps import Sitemap
from products.models import Product
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['home', 'profile', 'checkout']

    def location(self, item):
        return reverse(item)
