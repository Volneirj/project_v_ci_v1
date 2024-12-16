from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product



class TestBagViews(TestCase):

    def setUp(self):
        """
        Create test client and sample product for testing.
        """
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00
        )
        self.view_bag_url = reverse('view_bag')
        self.add_to_bag_url = reverse('add_to_bag', args=[self.product.id])
        self.adjust_bag_url = reverse('adjust_bag', args=[self.product.id])
        self.remove_from_bag_url = reverse('remove_from_bag', args=[self.product.id])

        # Add the product to the bag
        session = self.client.session
        session['bag'] = {str(self.product.id): 1}
        session.save()


    def test_view_bag(self):
        """
        Test rendering of bag view.
        """
        # Simulate a request
        response = self.client.get(self.view_bag_url)
        # Check if the page load succesfully
        self.assertEqual(response.status_code, 200)
        # Confirm template
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        """
        Test adding a product to the bag.
        """
        add_to_bag_url = reverse('add_to_bag', args=[self.product.id])
        
        # Send POST request to add product to the bag
        response = self.client.post(
            add_to_bag_url,
            {'quantity': 1, 'redirect_url': self.view_bag_url}
        )

        # Assert the response status code is 302 (redirection)
        self.assertEqual(response.status_code, 302)

        # Validate the bag in the session
        session = self.client.session
        self.assertIn(str(self.product.id), session['bag'])
        self.assertEqual(session['bag'][str(self.product.id)], 1)

        # Check the redirect location
        self.assertEqual(response.url, self.view_bag_url)

    def test_adjust_bag(self):
        """
        Test adjusting the bag to increase the quantity of an item.
        """
        # Simulate adding a product to the bag.
        response = self.client.post(
            self.adjust_bag_url,
            {'quantity': 3},
            follow=True
        )
        
        # Retrieve session data (Bag content)
        session = self.client.session

        # Check if has been updated for 3
        self.assertEqual(session['bag'][str(self.product.id)], 3)

        # Check the redirect location
        self.assertRedirects(response, self.view_bag_url)

    def test_adjust_bag_remove_item(self):
        """
        Test adjusting the bag to remove an item when quantity is 0.
        """
        # Simulate set the quantity to 0, that should remove the item
        response = self.client.post(
            self.adjust_bag_url,
            {'quantity': 0},
            follow=True
        )

        # Retrieve session data (Bag content)
        session = self.client.session

        # Check if the product Id no longer in the bag
        self.assertNotIn(str(self.product.id), session['bag'])

        # Check the redirect location
        self.assertRedirects(response, self.view_bag_url)

    def test_add_invalid_quantity(self):
        """
        Test adding an item with an invalid quantity.
        """
        # initialize a session
        session = self.client.session
        session['bag'] = {} # Clear bag for the test
        session.save()

        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': -1},  # Invalid quantity
            follow=True
        )

        # Refresh session after POST
        session = self.client.session

        # Check if the bag remains empty
        self.assertNotIn(str(self.product.id), session.get('bag', {}))

        # Verify that the response redirects properly
        self.assertRedirects(response, self.view_bag_url)
