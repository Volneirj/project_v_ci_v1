from django.test import TestCase
from home.models import Subscription


class TestSubscriptionModel(TestCase):
    def test_subscription_str(self):
        """Test the string representation of Subscription."""
        subscription = Subscription.objects.create(email="test@example.com")
        self.assertEqual(str(subscription), "test@example.com")
