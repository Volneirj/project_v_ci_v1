from django.db import models


class Subscription(models.Model):
    """
    A model to store subscriber details, including email and the timestamp
    of subscription.
    """
    email = models.EmailField(unique=True, verbose_name="Email Address")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Subscribed At")

    def __str__(self):
        return self.email
