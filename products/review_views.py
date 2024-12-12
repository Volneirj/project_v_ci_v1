"""
This file handle related views
used on product review
"""
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import OrderLineItem

from .models import Product, Review
from .forms import ReviewForm


def submit_review(request, product_id):
    """
    Handle product review submissions.
    """
    product = get_object_or_404(Product, id=product_id)

    # Ensure the user has purchased the product
    order_line_item = OrderLineItem.objects.filter(
        order__user_profile__user=request.user, product=product
    ).first()

    if not order_line_item:
        messages.error(
            request,
            "You can only review products you have purchased."
        )
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'order_line_item': order_line_item,
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment'],
                },
            )
            if created:
                messages.success(
                    request,
                    "Thank you for submitting your review!"
                    )
            else:
                messages.success(request, "Your review has been updated!")
        else:
            messages.error(
                request,
                "There was an error in your submission. Please try again."
                )
    return redirect('product_detail', product_id=product.id)


@login_required
def delete_review(request, review_id):
    """
    Allow users to delete their own reviews or
    admin to delete any review.
    """
    review = get_object_or_404(Review, id=review_id)

    # Allow the review's author or an admin to delete the review
    if request.user == review.user or request.user.is_superuser:
        review.delete()
        messages.success(request, "The review has been deleted.")
    else:
        messages.error(
            request,
            "You do not have permission to delete this review."
            )

    return redirect('product_detail', product_id=review.product.id)
