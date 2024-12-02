from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from home.models import Categories, Products, Offers, Transanction
from datetime import datetime

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a superuser and a regular user
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='password')
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='password')

        # Create a category for testing
        self.category = Categories.objects.create(name="Test Category")

        # Create a product for testing
        self.product = Products.objects.create(
            name="Test Product",
            price=100,
            description="Test Description",
            category=self.category,
            discount=10,
            discounted_price=90,
            image = "C:\\Users\\HP\\Desktop\\Course Materials\\7. 6th Semester (Summer-24)\\CSE327\\Project\\Code\\ShopEasy-Your-Favourite-Ecommerce-Platform\\eCommerceWebsite\\home\\static\\images\\kb2.jpeg"
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {'email': 'user@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'wrong@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'password': 'password',
            'c_password': 'password',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser@example.com').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'password': 'password1',
            'c_password': 'password2',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)

    def test_log_out(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_add_products_superuser(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('add_products'), {
            'name': 'New Product',
            'price': 200,
            'description': 'New Description',
            'category': self.category.id,
            'discount': 20,
            "img": ""
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Products.objects.filter(name='New Product').exists())

    def test_add_products_not_admin(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('add_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not an Admin")

    def test_add_offers_superuser(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('add_offers', args=[self.product.id]), {
            'discount': 15,
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.discount, 15)
        self.assertEqual(self.product.discounted_price, 85)

    def test_view_dashboard(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('view_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_user_dashboard_authenticated(self):
        self.client.login(username='testuser', password='password')
        Transanction.objects.create(user=self.user.username, amount=200, date=datetime.today())
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "200.0")

    def test_user_dashboard_unauthenticated(self):
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
