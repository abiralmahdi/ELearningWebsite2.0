from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Categories, Offers, Products, Cart, Transanction, Contact

class ViewsTestCase(TestCase):
    def setUp(self):
        # Set up test client and data
        self.client = Client()
        self.user = User.objects.create_user(username='testuser@test.com', password='password')
        self.category = Categories.objects.create(name='Electronics', description='Electronic items')
        self.product = Products.objects.create(
            name='Laptop', description='Gaming Laptop', price=1000, discount=10,
            category=self.category
        )
        self.cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.offer = Offers.objects.create(
            product=self.product, discount=10, start_date='2023-01-01', end_date='2023-12-31'
        )

    def test_home_view(self):
        # Test unauthenticated access
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        # Test authenticated access
        self.client.login(username='testuser@test.com', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        self.assertIn('offers', response.context)
        self.assertIn('cart_items', response.context)

    def test_contact_view(self):
        # Test GET request
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

        # Test POST request
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.',
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Contact.objects.count(), 1)


    def test_products_page_view(self):
        response = self.client.get(reverse('products_page', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.context)

    def test_indiv_product_view(self):
        response = self.client.get(reverse('indiv_product', args=[self.category.id, self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('product', response.context)


    def test_add_to_cart_view(self):
        self.client.login(username='testuser@test.com', password='password')
        response = self.client.post(reverse('add_to_cart', args=[self.product.id, 3]))
        self.assertEqual(response.status_code, 302)
        

