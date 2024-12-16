from django.test import TestCase
from checkout.models import Order, OrderLineItem
from products.models import Product


class TestOrderSignals(TestCase):
    def setUp(self):
        self.order = Order.objects.create(full_name="John Doe")
        self.product = Product.objects.create(name="Test Product", price=10)
        self.lineitem = OrderLineItem.objects.create(
            order=self.order, product=self.product, quantity=2)

    def test_save_no_delivery(self):
        """Verify order total updates when a lineitem is saved."""
        self.lineitem.quantity = 3
        self.lineitem.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, 30)

    def test_save_order_delivery(self):
        """Verify grand total updates when a lineitem is saved."""
        self.lineitem.quantity = 3
        self.lineitem.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.grand_total, 33)

    def test_update_on_delete(self):
        """Verify grand total updates when a lineitem is deleted."""
        self.lineitem.delete()
        self.order.refresh_from_db()
        self.assertEqual(self.order.grand_total, 0)
