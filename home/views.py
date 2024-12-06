"""Home views setup"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubscriptionForm


def index(request):
    """
    A view to return the index page
    """
    return render(request, 'home/index.html')


def subscribe(request):
    """
    Handle the subscription form submission.
    - Validates and saves the email if it is unique and properly formatted.
    - Displays success or error messages based on the result.

    Args:
        request: The HTTP request object containing form data.

    Returns:
        A redirect to the home page.
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
        else:
            messages.error(request, "Invalid email or already subscribed.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))
