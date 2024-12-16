from django.test import TestCase
from products.models import Product, Category, Wishlist, Review
from django.contrib.auth.models import User


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00,
            category=self.category,
            rating=4.0
        )

    def test_average_rating_with_reviews(self):
        """Test average_rating with reviews."""
        user1 = User.objects.create_user(username="test1")
        user2 = User.objects.create_user(username="test2")
        Review.objects.create(product=self.product, user=user1, rating=5)
        Review.objects.create(product=self.product, user=user2, rating=3)

        self.assertEqual(self.product.average_rating, 4.0)

    def test_average_rating_without_reviews(self):
        """Test average_rating fallback to product's rating."""
        self.assertEqual(self.product.average_rating, 4.0)


class TestWishlistModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.product = Product.objects.create(name="Test Product", price=30.00)

    def test_unique_together(self):
        """Test that duplicate wishlist entries are not allowed."""
        Wishlist.objects.create(user=self.user, product=self.product)
        with self.assertRaises(Exception):
            Wishlist.objects.create(user=self.user, product=self.product)


class TestReviewModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.product = Product.objects.create(name="Test Product", price=30.00)

    def test_rating_constraints(self):
        """Test rating constraints between 0 and 5."""
        # Valid rating (should not raise an error)
        review = Review(product=self.product, user=self.user, rating=4)
        try:
            review.full_clean()  # Trigger the model validation
        except Exception:
            self.fail("full_clean() raised Exception unexpectedly!")

        # Invalid rating (above 5)
        review_invalid_high = Review(
            product=self.product, user=self.user, rating=6)
        with self.assertRaises(Exception):
            review_invalid_high.full_clean()

        # Invalid rating (below 0)
        review_invalid_low = Review(
            product=self.product, user=self.user, rating=-1)
        with self.assertRaises(Exception):
            review_invalid_low.full_clean()
