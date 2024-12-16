from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category, Wishlist, Review
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem
from django.test import TestCase, Client


class TestProductViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.admin = User.objects.create_superuser(
            username="admin", password="password")
        self.category = Category.objects.create(name="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00,
            category=self.category
        )

    def test_all_products_view(self):
        """Test all products view renders correctly."""
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        """Test product detail view."""
        response = self.client.get(reverse(
            'product_detail', args=[self.product.id]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_add_product_admin_only(self):
        """Test only admin can add a product."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, reverse('home'))

        self.client.login(username="admin", password="password")
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_wishlist_view_authenticated(self):
        """Test adding a product to wishlist."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse('wishlist'),
            {'product_id': self.product.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Wishlist.objects.filter(
            user=self.user, product=self.product
        ).exists())


class TestSubmitReviewView(TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        # Ensure UserProfile exists
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

        # Create product and order
        self.product = Product.objects.create(
            name="Test Product", price=20.00)
        self.order = Order.objects.create(
            user_profile=self.profile, original_bag="{}")
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order, product=self.product)

    def test_submit_review(self):
        """Test submitting a review for a purchased product."""
        response = self.client.post(
            reverse('submit_review', args=[self.product.id]),
            {'rating': 4, 'comment': 'Great product!'}
        )

        # Verify the user is redirected to the product detail page
        self.assertRedirects(response, reverse(
            'product_detail',
            args=[self.product.id]
        ))

        # Check that the review was created
        review = Review.objects.filter(
            product=self.product,
            user=self.user
        ).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Great product!')
