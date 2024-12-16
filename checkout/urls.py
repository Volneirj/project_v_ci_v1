"""
Checkout URL settings.
"""
from django.urls import path
from . import views
from .webhooks import webhook
from .order_views import order_management, order_detail

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_success/<order_number>',
        views.checkout_success,
        name='checkout_success'
        ),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'
        ),
    path('wh/', webhook, name='webhook'),
    path('orders/', order_management, name='orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
]
