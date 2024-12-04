"""
Product URLs settings
"""

from django.urls import path
from .views import WishlistView, wishlist_page, remove_from_wishlist
from . import views



urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product,
         name='delete_product'
         ),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist_page/', wishlist_page, name='wishlist_page'),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
