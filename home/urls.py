"""
Home URL settings.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('our_story/', views.our_story, name='our_story'),
]
