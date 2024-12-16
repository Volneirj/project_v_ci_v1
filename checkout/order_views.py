from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order


@staff_member_required
def order_management(request):
    """
    View to display all orders for management purposes.
    """
    orders = Order.objects.all().order_by('-date')
    return render(request, 'checkout/orders.html', {'orders': orders})


@staff_member_required
def order_detail(request, order_id):
    """
    View to display the details of a specific order.

    - Requires the user to be a staff member.
    - Fetches the order based on the provided `order_id`.
    - Retrieves all line items related to the order.
    - Constructs a delivery information dictionary for display.
    - Renders the 'order_detail.html' template with
    order details and line items.

    Args:
        request: The HTTP request object.
        order_id (int): The ID of the specific order to display.

    Returns:
        HttpResponse: Renders the order detail page with
        the specific order data.

    Raises:
        Http404: If the order with the given ID does not exist.
    """
    order = get_object_or_404(Order, id=order_id)
    lineitems = order.lineitems.all()

    delivery_info = {
        "Full Name": order.full_name,
        "Address 1": order.street_address1,
        "Address 2": order.street_address2 or "N/A",
        "Town or City": order.town_or_city,
        "Postal Code": order.postcode or "N/A",
        "Country": order.country,
        "Phone Number": order.phone_number,
    }

    context = {
        'order': order,
        'lineitems': lineitems,
        'delivery_info': delivery_info,
    }
    return render(request, 'checkout/order_detail.html', context)
