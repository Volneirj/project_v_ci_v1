from django.test import TestCase
from django.urls import reverse
from django.core import mail
from home.models import Subscription
from django.test import override_settings


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    EMAIL_HOST_USER='test@example.com'
)
class TestHomeViews(TestCase):
    def test_index_view(self):
        """Test that the index page renders correctly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_static_pages(self):
        """Test static pages render with correct templates."""
        pages = [
            {'url': reverse(
                'our_story'), 'template': 'home/our_story.html'},
            {'url': reverse(
                'faqs'), 'template': 'home/faqs.html'},
            {'url': reverse(
                'privacy_policy'), 'template': 'home/privacy_policy.html'},
            {'url': reverse(
                'terms_conditions'), 'template': 'home/terms_conditions.html'},
            {'url': reverse(
                'workshops'), 'template': 'home/workshops.html'},
        ]
        for page in pages:
            response = self.client.get(page['url'])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, page['template'])

    def test_subscribe_valid(self):
        """Test successful subscription form submission."""
        response = self.client.post(
            reverse('subscribe'), {'email': 'test@example.com'})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(
            Subscription.objects.filter(email='test@example.com').exists())

    def test_subscribe_invalid(self):
        """Test invalid subscription form submission."""
        # Post an invalid email
        response = self.client.post(
            reverse('subscribe'), {'email': 'invalid-email'})
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(
            Subscription.objects.filter(email='invalid-email').exists())

    def test_contact_us_get(self):
        """Test that the Contact Us form is displayed on GET."""
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact_us.html')

    def test_contact_us_post_valid(self):
        """Test valid Contact Us form submission sends an email."""
        response = self.client.post(reverse('contact_us'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content.',
        })
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact_us.html')

        # Check if email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertIn('Test message content.', mail.outbox[0].body)

    def test_contact_us_post_invalid(self):
        """Test invalid Contact Us form submission."""
        response = self.client.post(reverse('contact_us'), {
            'name': '',
            'email': 'not-an-email',
            'subject': '',
            'message': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact_us.html')
        self.assertContains(
            response, "There was an error. Please check the form.")
