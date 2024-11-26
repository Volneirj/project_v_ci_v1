import json
import time

import stripe
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class StripeWebHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        try:
            cust_email = order.email

            subject = render_to_string(
                'checkout/confirmation_emails/confirmation_email_subject.txt',
                {'order': order}
            ).strip()

            body = render_to_string(
                'checkout/confirmation_emails/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
            )

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email],
                fail_silently=False,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Error sending confirmation email for order {order.order_number}: {e}")
            pass

    def _get_stripe_charge_and_details(self, intent):
        """Retrieve charge details from Stripe"""
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            charge = stripe.Charge.retrieve(intent.latest_charge)
            billing_details = charge.billing_details
            shipping_details = intent.shipping
            grand_total = round(charge.amount / 100, 2)
            return charge, billing_details, shipping_details, grand_total
        except stripe.error.StripeError as e:
            raise ValueError(f"Stripe error: {e}") from e

    def _update_user_profile(self, shipping_details, username, save_info):
        """Update user profile information if save_info is checked"""
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)  # pylint: disable=E1101
                if save_info:
                    address = shipping_details['address']  # Extract the dictionary
                    profile.default_phone_number = shipping_details.get('phone')
                    profile.default_country = address.get('country')
                    profile.default_postcode = address.get('postal_code')
                    profile.default_town_or_city = address.get('city')
                    profile.default_street_address1 = address.get('line1')
                    profile.default_street_address2 = address.get('line2')
                    profile.default_county = address.get('state')
                    profile.save()
                return profile
            except ObjectDoesNotExist:
                pass
        return None

    def _create_order(self, order_data, profile=None):
        """Create an order and its line items"""
        try:
            order = Order.objects.create(  # pylint: disable=E1101
                full_name=order_data["shipping_details"].name,
                user_profile=profile,
                email=order_data["billing_details"].email,
                phone_number=order_data["shipping_details"].phone,
                country=order_data["shipping_details"].address.country,
                postcode=order_data["shipping_details"].address.postal_code,
                town_or_city=order_data["shipping_details"].address.city,
                street_address1=order_data["shipping_details"].address.line1,
                street_address2=order_data["shipping_details"].address.line2,
                county=order_data["shipping_details"].address.state,
                original_bag=order_data["bag"],
                stripe_pid=order_data["pid"],
                grand_total=order_data["grand_total"],
            )
            for item_id, item_data in json.loads(order_data["bag"]).items():
                product = Product.objects.get(id=item_id)  # pylint: disable=E1101
                if isinstance(item_data, int):
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                else:
                    for size, quantity in item_data["items_by_size"].items():
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )
                        order_line_item.save()
            return order
        except Exception as e:
            if 'order' in locals() and order:
                order.delete()
            raise ValueError(f"Order creation failed: {e}") from e


    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.get('bag', None)
        save_info = intent.metadata.get('save_info', 'false')  # Default to 'false'

        if not bag:
            return HttpResponse(
                content="Webhook received but 'bag' metadata is missing.",
                status=400,
            )
        # Retrieve charge and details
        try:
            (
                billing_details,
                shipping_details,
                grand_total
                )= self._get_billing_shipping_details(intent)
        except ValueError as e:
            return HttpResponse(content=str(e), status=500)

        # Clean shipping details
        shipping_details['address'] = {
            field: (value if value != "" else None)
            for field, value in shipping_details['address'].items()
        }

        # Update user profile
        profile = self._update_user_profile(
            shipping_details, intent.metadata.username, save_info
        )

        # Consolidate order search parameters
        order_search_params = {
            "full_name__iexact": shipping_details['name'],
            "email__iexact": billing_details['email'],
            "phone_number__iexact": shipping_details.get('phone'),
            "country__iexact": shipping_details['address'].get('country'),
            "postcode__iexact": shipping_details['address'].get('postal_code'),
            "town_or_city__iexact": shipping_details['address'].get('city'),
            "street_address1__iexact": shipping_details['address'].get('line1'),
            "street_address2__iexact": shipping_details['address'].get('line2'),
            "county__iexact": shipping_details['address'].get('state'),
            "grand_total": grand_total,
            "original_bag": bag,
            "stripe_pid": pid,
        }
                
        
        # Try to find an existing order
        order = self._find_existing_order(order_search_params)
        if order:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |'
                        f' SUCCESS: Verified order already in database',
                status=200,
            )

        # Create a new order
        order_data = {
            "shipping_details": shipping_details,
            "billing_details": billing_details,
            "bag": bag,
            "grand_total": grand_total,
            "pid": pid,
        }

        try:
            order = self._create_order(order_data, profile)
        except ValueError as e:
            return HttpResponse(content=str(e), status=500)

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200,
        )


    def _get_billing_shipping_details(self, intent):
        """Retrieve and return billing and shipping details"""
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            charge = stripe.Charge.retrieve(intent.latest_charge)  # Unused variable removed
            billing_details = charge.billing_details
            shipping_details = intent.shipping
            grand_total = round(charge.amount / 100, 2)
            return billing_details, shipping_details, grand_total
        except stripe.error.StripeError as e:
            raise ValueError(f"Stripe error: {e}") from e


    def _find_existing_order(self, order_search_params):
        """Try to find an existing order based on the search parameters"""
        attempt = 1
        while attempt <= 5:
            try:
                return Order.objects.get(**order_search_params)  # pylint: disable=E1101
            except Order.DoesNotExist:  # pylint: disable=E1101
                attempt += 1
                time.sleep(1)
        return None

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
