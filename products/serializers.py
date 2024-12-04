from rest_framework import serializers
from .models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wishlist model.

    Adds additional product-related fields (name, price, image URL) for convenience when rendering
    wishlist data in the API.

    Fields:
        - id: The unique ID of the wishlist entry.
        - user: The user who owns the wishlist entry.
        - product: The product in the wishlist.
        - product_name: The name of the product (read-only).
        - product_price: The price of the product (read-only).
        - product_image_url: The URL of the product's image (read-only).
        - created_at: The timestamp when the wishlist entry was created (read-only).
    """   
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image_url = serializers.ImageField(source='product.image.url', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'product_image_url', 'created_at']
        read_only_fields = ['user', 'created_at']