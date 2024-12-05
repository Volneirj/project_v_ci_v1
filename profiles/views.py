"""
Source code from Boutique Ado walkthrough.

Refactored for better readability, maintainability, and compliance with
Django best practices.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User

from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
@ensure_csrf_cookie
def profile(request):
    """ Display the user's profile. """
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
        if email and request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')

        return redirect('profile')  # Redirect to the profile page after POST
    else:
        form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Get order history
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
