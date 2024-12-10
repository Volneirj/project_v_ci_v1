"""
Source code:boutiqueado walkthrough
"""

from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """
    Retrieve the contents of the shopping bag from the session and calculate totals.

    This function computes the total price, product count, delivery costs,
    and other bag-related metrics. It prepares a list of items in the bag,
    where each item includes its ID, quantity, and corresponding product details.
    It also calculates the delivery cost based on the total price and
    whether the free delivery threshold has been met.

    Args:
        request (HttpRequest): The HTTP request object, which includes
        session data.

    Returns:
        dict: A dictionary containing:
            - bag_items: List of items in the bag, each with item_id, quantity, and product details.
            - total: Total cost of all items in the bag.
            - product_count: Total number of items in the bag.
            - delivery: Delivery cost based on the total price.
            - free_delivery_delta: Amount required to qualify for free delivery.
            - free_delivery_threshold: The minimum total required for free delivery.
            - grand_total: Total cost including delivery.
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
