from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal for a given price and quantity.

    Args:
        price (Decimal or float): The price of the product.
        quantity (int): The quantity of the product.

    Returns:
        Decimal or float: The subtotal (price * quantity).
    """
    return price * quantity
