from django.test import TestCase
from checkout.models import Order, OrderLineItem
from products.models import Product
from django.conf import settings


class TestOrderModel(TestCase):
    def setUp(self):
        # Create a product for testing line items
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00
        )
        # Create an order for testing
        self.order = Order.objects.create(
            full_name="John Doe",
            email="john@example.com",
            phone_number="123456789",
            country="US",
            town_or_city="New York",
            street_address1="123 Main St",
            original_bag='{"1": 2}',
        )

    def test_generate_order_number(self):
        """Ensure the order number is generated when an order is saved."""
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(len(self.order.order_number), 32)

    def test_update_total_below_free_delivery(self):
        """Verify grand_total and delivery_cost when
        below free delivery threshold."""
        settings.FREE_DELIVERY_THRESHOLD = 50
        settings.STANDARD_DELIVERY_PERCENTAGE = 10
        OrderLineItem.objects.create(
            order=self.order, product=self.product, quantity=1)
        self.order.update_total()
        self.assertEqual(self.order.order_total, 20.00)  # 1 * 20
        self.assertEqual(self.order.delivery_cost, 2.00)  # 10% of 20
        self.assertEqual(self.order.grand_total, 22.00)  # order_total+delivery

    def test_update_total_above_free_delivery(self):
        """Verify no delivery cost is added when above
          the free delivery threshold."""
        settings.FREE_DELIVERY_THRESHOLD = 50
        settings.STANDARD_DELIVERY_PERCENTAGE = 10
        OrderLineItem.objects.create(
            order=self.order, product=self.product, quantity=3)
        self.order.update_total()
        self.assertEqual(self.order.order_total, 60.00)  # 3 * 20
        self.assertEqual(self.order.delivery_cost, 0.00)  # Free delivery
        self.assertEqual(self.order.grand_total, 60.00)


class TestOrderLineItemModel(TestCase):
    def setUp(self):
        # Create a product and order for testing
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00
        )
        self.order = Order.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            phone_number="987654321",
            country="US",
            town_or_city="Los Angeles",
            street_address1="456 Elm St",
        )

    def test_lineitem_total_calculation(self):
        """Ensure lineitem_total is calculated correctly and saved."""
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(lineitem.lineitem_total, 40.00)  # 2 * 20
