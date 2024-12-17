"""
Home URL settings.
"""
from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap, StaticViewSitemap

sitemaps = {
    'products': ProductSitemap(),
    'static': StaticViewSitemap(),
}

urlpatterns = [
    path('', views.index, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('our_story/', views.our_story, name='our_story'),
    path('shipping-returns/', views.shipping_returns, name='shipping_returns'),
    path('faqs/', views.faqs, name='faqs'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('workshops/', views.workshops, name='workshops'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
