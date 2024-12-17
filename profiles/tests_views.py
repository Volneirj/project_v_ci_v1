from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order


class TestProfileViews(TestCase):
    def setUp(self):
        """Set up a user and order for testing."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")
        self.profile = UserProfile.objects.get(user=self.user)
        self.order = Order.objects.create(
            user_profile=self.profile,
            order_number="12345",
            original_bag="{}"
        )

    def test_profile_view_get(self):
        """Test that the profile page renders for a logged-in user."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_update_post(self):
        """Test that a profile update works successfully."""
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '1234567890',
            'default_town_or_city': 'New York',
            'default_street_address1': '123 Main St',
            'email': 'newemail@example.com',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.profile.default_phone_number, '1234567890')

    def test_order_history_view(self):
        """Test the order history view renders correctly."""
        response = self.client.get(reverse(
            'order_history', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, self.order.order_number)
