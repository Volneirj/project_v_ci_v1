"""
This file handle the models related to the home page
and for future implementations.
"""
from django.db import models
from profiles.models import UserProfile


class Subscription(models.Model):
    """
    A model to store subscriber details, including email and the timestamp
    of subscription.
    """
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subscription"
    )
    email = models.EmailField(unique=True, verbose_name="Email Address")
    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Subscribed At",
    )

    def __str__(self):
        return str(self.email)
