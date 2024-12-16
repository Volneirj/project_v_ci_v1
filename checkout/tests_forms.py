from django.test import TestCase
from checkout.forms import OrderForm


class TestOrderForm(TestCase):
    def test_valid_order_form(self):
        """Ensure the form validates with correct data."""
        form_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "street_address1": "123 Main St",
            "town_or_city": "New York",
            "country": "US",
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_placeholders(self):
        """Verify placeholders and attributes are set correctly."""
        form = OrderForm()
        self.assertEqual(
            form.fields["full_name"].widget.attrs["placeholder"],
            "Full Name *"
        )
