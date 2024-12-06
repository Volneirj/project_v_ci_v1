from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Subscription model.
    Displays the email and subscription date in the admin list view.
    """
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
