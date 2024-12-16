from django.test import TestCase
from home.forms import SubscriptionForm, ContactUsForm


class TestSubscriptionForm(TestCase):
    def test_valid_form(self):
        """Test valid subscription form."""
        form = SubscriptionForm(data={'email': 'test@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test invalid subscription form."""
        form = SubscriptionForm(data={'email': 'invalid-email'})
        self.assertFalse(form.is_valid())


class TestContactUsForm(TestCase):
    def test_valid_form(self):
        """Test valid Contact Us form."""
        form = ContactUsForm(data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content.',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test invalid Contact Us form."""
        form = ContactUsForm(data={
            'name': '',
            'email': 'not-an-email',
            'subject': '',
            'message': '',
        })
        self.assertFalse(form.is_valid())
