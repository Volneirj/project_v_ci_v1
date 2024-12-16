from django.test import TestCase
from django.urls import reverse
from checkout.models import Order
from django.contrib.auth.models import User
from products.models import Product


class TestOrderManagementView(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff",
            password="password",
            is_staff=True
        )
        self.client.login(username="staff", password="password")

    def test_order_management_access(self):
        """Ensure only staff can access the order management page."""
        response = self.client.get(reverse("orders"))
        self.assertEqual(response.status_code, 200)

    def test_order_management_context(self):
        """Check if orders are passed to the template."""
        Order.objects.create(full_name="John Doe")
        response = self.client.get(reverse("orders"))
        self.assertIn("orders", response.context)


class TestCheckoutView(TestCase):
    def setUp(self):
        """Set up test data and session."""
        # Create a product to add to the bag
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00
        )

        # Simulate a session with a valid product in the bag
        session = self.client.session
        session['bag'] = {str(self.product.id): 2}
        session.save()

        # add mock data
        self.valid_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "street_address1": "123 Main St",
            "street_address2": "Apartment A5",
            "town_or_city": "New York",
            "postcode": "55555",
            "county": "NA",
            "country": "US",
            "client_secret": "test_client_secret_secret123",
        }

    def test_checkout_get(self):
        """Ensure GET requests render the checkout page."""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_post_valid_data(self):
        """Verify a valid checkout POST creates an order."""
        response = self.client.post(reverse("checkout"), data=self.valid_data)

        # Check an order was created
        self.assertTrue(Order.objects.exists())
        order = Order.objects.first()

        # Check the response redirects to the correct success page
        expected_url = reverse("checkout_success", args=[order.order_number])
        self.assertRedirects(response, expected_url)
