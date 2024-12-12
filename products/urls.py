"""
Product URLs settings
"""

from django.urls import path
from .views import WishlistView, wishlist_page, remove_from_wishlist
from . import views, review_views


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete_product/<int:product_id>/',
        views.delete_product,
        name='delete_product'
        ),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist_page/', wishlist_page, name='wishlist_page'),
    path(
        'wishlist/remove/<int:item_id>/',
        remove_from_wishlist,
        name='remove_from_wishlist'
        ),
    path(
        'product/<int:product_id>/submit_review/',
        review_views.submit_review,
        name='submit_review'
        ),
    path(
        'review/<int:review_id>/delete/',
        review_views.delete_review,
        name='delete_review'
        ),
]
