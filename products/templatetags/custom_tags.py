from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating):
    """
    Renders HTML for a star rating and marks it as safe.
    Generate the amount of start yellow for rating and white for left stars.
    """
    full_stars = '<i class="fas fa-star text-warning"></i>' * int(rating)
    empty_stars = '<i class="far fa-star text-warning"></i>' * (5 - int(rating))
    return mark_safe(full_stars + empty_stars)
