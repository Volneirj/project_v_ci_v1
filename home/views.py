"""Home views setup"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SubscriptionForm, ContactUsForm


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


def shipping_returns(request):
    """
    Render the Shipping & Returns page.

    This view handles displaying information about the shipping policies,
    including processing times, delivery options, and return policies.
    """
    return render(request, 'home/shipping_returns.html')


def faqs(request):
    """
    Render the Frequently Asked Questions (FAQs) page.

    This view handles displaying common questions and answers related to
    orders, shipping, returns, products, and payment.
    """
    return render(request, 'home/faqs.html')


def privacy_policy(request):
    """
    Render the Privacy Policy page.

    This view displays the privacy policy of the website, outlining how
    user data is collected, stored, used, and protected.
    """
    return render(request, 'home/privacy_policy.html')


def terms_conditions(request):
    """
    Render the Terms & Conditions page.

    This view displays the terms of use for the website, including the
    rules and regulations for accessing and using the platform.
    """
    return render(request, 'home/terms_conditions.html')


def workshops(request):
    """
    Render the Workshops page.

    This view displays information about upcoming workshops, including
    details on how to participate and what to expect.
    """
    return render(request, 'home/workshops.html')


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

    # Validate HTTP_REFERER
    referer = request.META.get('HTTP_REFERER')
    if (
        referer
        and url_has_allowed_host_and_scheme(
            referer, allowed_hosts={request.get_host()}
        )
    ):
        return redirect(referer)
    return redirect('home')


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
            messages.error(request,
                           "There was an error. Please check the form.")
    else:
        form = ContactUsForm()

    return render(request, 'home/contact_us.html', {'form': form})
