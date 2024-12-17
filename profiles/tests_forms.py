from django.test import TestCase
from profiles.forms import UserProfileForm


class TestUserProfileForm(TestCase):
    def test_valid_userprofile_form(self):
        """Test the UserProfileForm with valid data."""
        form = UserProfileForm(data={
            'default_phone_number': '1234567890',
            'default_postcode': '12345',
            'default_town_or_city': 'New York',
            'default_street_address1': '123 Main St',
            'default_street_address2': '',
            'default_county': 'NY',
            'default_country': 'US',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_userprofile_form(self):
        """Test the UserProfileForm with invalid data."""
        form = UserProfileForm(data={
            'default_phone_number': 'aaaaa',
            'default_country': '----',
        })
        self.assertFalse(form.is_valid())
