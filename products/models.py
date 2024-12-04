"""
Category and products Source of code: 
Boutiqueado walkthrought.

Refactored for better readability, maintainability, 
and compliance with Django best practices.

"""
from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Represents a product category, 
    with an optional friendly name for display purposes.
    """

    class Meta:
        verbose_name_plural= 'Categories'

    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null = True, blank = True, verbose_name="Friendly Name")

    def __str__(self):
        return str(self.name)
    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    """
    Represents a product, linked to a category and with additional details
    such as price, rating, and optional image fields.
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField (default = False, null = True, blank = True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
    

class Wishlist(models.Model):
    """
    Model representing a user's wishlist.

    Attributes:
        user (ForeignKey): A reference to the user who owns the wishlist.
        product (ForeignKey): A reference to the product added to the wishlist.    
    Meta:
        unique_together: Ensures the item is not added twice.
        ordering: Orders wishlist items by creation date in descending order.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
