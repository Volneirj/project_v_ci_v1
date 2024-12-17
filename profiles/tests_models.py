from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestUserProfileModel(TestCase):
    def setUp(self):
        """Set up a user and profile for testing."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.profile = UserProfile.objects.get(user=self.user)
        self.client.login(username="testuser", password="password123")

    def test_userprofile_created(self):
        """Test that a UserProfile is created
        automatically when a User is created."""
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(user_profile)

    def test_userprofile_fields(self):
        """Test default fields in UserProfile."""
        profile = UserProfile.objects.get(user=self.user)

        # Assert that default fields are None when no values are provided
        self.assertIsNone(profile.default_phone_number,
                          "Phone number should default to None")
        self.assertIsNone(profile.default_street_address1,
                          "Street address 1 should default to None")
        self.assertIsNone(profile.default_street_address2,
                          "Street address 2 should default to None")
        self.assertIsNone(profile.default_town_or_city,
                          "Town or city should default to None")
        self.assertIsNone(profile.default_county,
                          "County should default to None")
        self.assertIsNone(profile.default_postcode,
                          "Postcode should default to None")
        self.assertIsNone(profile.default_country,
                          "Country should default to None")
