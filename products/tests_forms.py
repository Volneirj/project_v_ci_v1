from django.test import TestCase
from products.forms import ProductForm, ReviewForm


class TestProductForm(TestCase):
    def test_valid_product_form(self):
        """Test product form with valid data."""
        form = ProductForm(data={
            'name': 'Test Product',
            'price': 10.00,
            'description': 'This is a test product',
            'sku': '12345',
        })
        self.assertTrue(form.is_valid())

    def test_product_form_saves(self):
        """Test that the product form saves correctly."""
        form = ProductForm(data={
            'name': 'Test Product',
            'price': 10.00,
            'description': 'This is a test product',
            'sku': '12345',
        })
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, 'Test Product')

    def test_review_form_valid(self):
        """Test valid review form."""
        form = ReviewForm(data={'rating': 4, 'comment': 'Great!'})
        self.assertTrue(form.is_valid())
