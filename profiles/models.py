"""
Source of code : Boutiqueado walkthrought.

Refactored for better readability, maintainability, and compliance with
Django best practices.
"""
import pycountry

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_country_choices():
    """
    Generate a list of country choices with a blank label at the top.
    """
    choices = [("", "Select your country")]
    choices += [
        (country.alpha_2, country.name) for country in pycountry.countries]
    return choices


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = models.CharField(
        max_length=2,
        choices=get_country_choices(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
