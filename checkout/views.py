import json
import stripe

from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    """
    Update the Stripe PaymentIntent with metadata.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username if request.user.is_authenticated else 'Guest',
        })
        return HttpResponse(status=200)
    except stripe.error.StripeError as e:
        messages.error(
            request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)

@ensure_csrf_cookie
def checkout(request):
    """
    Handle checkout requests (GET and POST).
    """
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        return handle_post_checkout(request)

    return handle_get_checkout(request, stripe_secret_key)


def handle_post_checkout(request):
    """
    Handle POST logic for checkout.
    """
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect(reverse('products'))

    form_data = {field: request.POST[field] for field in OrderForm.Meta.fields}
    order_form = OrderForm(form_data)

    if order_form.is_valid():
        order = _create_order(request, order_form, bag)
        if not order:
            return redirect(reverse('view_bag'))

        request.session['save_info'] = 'save-info' in request.POST
        return redirect(reverse('checkout_success', args=[order.order_number]))

    messages.error(
        request, "There was an error with your form. Please double-check your information.")
    return redirect(reverse('checkout'))


def handle_get_checkout(request, stripe_secret_key):
    """
    Handle GET logic for checkout.
    """
    # Get the shopping bag from the session
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('products'))

    # Calculate the current bag totals
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    # Create a PaymentIntent with metadata
    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        metadata={
            'bag': json.dumps(request.session.get('bag', {})),  # Include bag
            'save_info': request.POST.get('save_info', 'false'),  # Include save_info
            'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
        },
    )

    # Initialize the order form
    order_form = _initialize_order_form(request)

    # Get the Stripe public key
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    if not stripe_public_key:
        messages.warning(
            request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    # Render the checkout page with context
    return render(request, 'checkout/checkout.html', {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    })

def checkout_success(request, order_number):
    """
    Handle successful checkouts.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user) # pylint: disable=no-member
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                field: getattr(order, field)
                for field in OrderForm.Meta.fields if hasattr(order, field)
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request, f'Order successfully processed! Your order number '
        f'is {order_number}. A confirmation email will be sent to {order.email}.')
    request.session.pop('bag', None)

    return render(request, 'checkout/checkout_success.html', {'order': order})


def _initialize_order_form(request):
    """
    Initialize the order form with user profile data if available.
    """
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user) # pylint: disable=no-member
            initial_data = {
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            }
            return OrderForm(initial=initial_data)
        except UserProfile.DoesNotExist: # pylint: disable=no-member
            return OrderForm()
    else:
        return OrderForm()


def _create_order(request, order_form, bag):
    """
    Create an order and its line items from the bag.
    """
    try:
        order = order_form.save(commit=False)
        pid = request.POST.get('client_secret').split('_secret')[0]
        order.stripe_pid = pid
        order.original_bag = json.dumps(bag)
        order.save()

        for item_id, item_data in bag.items():
            product = Product.objects.get(id=item_id) # pylint: disable=no-member
            if isinstance(item_data, int):
                OrderLineItem.objects.create(order=order, product=product, quantity=item_data) # pylint: disable=no-member
            else:
                for size, quantity in item_data['items_by_size'].items():
                    OrderLineItem.objects.create( # pylint: disable=no-member
                        order=order, product=product, quantity=quantity, product_size=size
                        )

        return order
    except Product.DoesNotExist: # pylint: disable=no-member
        messages.error(request, (
                       "One of the products in your bag "
                       "wasn't found in our database. Please call us for assistance."
                       ))
        order.delete()
        return None
