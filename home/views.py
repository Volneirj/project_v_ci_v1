"""Home views setup"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SubscriptionForm, ContactUsForm
from django.conf import settings


def index(request):
    """
    A view to return the index page
    """
    return render(request, 'home/index.html')


def our_story(request):
    """
    A view to return the our_story page
    """
    return render(request, 'home/our_story.html')


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


def contact_us(request):
    """
    Handle the Contact Us form submission via email.
    """
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Send an email
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                [settings.EMAIL_HOST_USER],
            )
            messages.success(request, "Your message has been sent. Thank you!")
            form = ContactUsForm()
        else:
            messages.error(request, "There was an error. Please check the form.")
    else:
        form = ContactUsForm()

    return render(request, 'home/contact_us.html', {'form': form})

