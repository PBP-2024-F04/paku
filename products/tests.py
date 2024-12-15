from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product
from products.forms import ProductForm

User = get_user_model()

# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testUser", password="testPass", role="Merchant")
        self.product = Product.objects.create(
            user=self.user,
            product_name="Test Product",
            restaurant="Test Restaurant",
            price=1000,
            description="Test Description",
            category="Test Category"
        )
        self.client.login(username='testUser', password='testPass', role="Merchant")
        self.my_products_url = reverse('products:my_products')

    def test_create_product(self):
        self.client.login(username="testUser", password="testPass")
        response = self.client.post(reverse('products:create_product'), {
            'product_name': 'Bubur Ayam',
            'restaurant': 'RM Palu',
            'price': 10000,
            'description': 'Terbuat dari nasi piihan',
            'category': 'Indonesian'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_edit_product(self):
        product = Product.objects.create(
            user=self.user,
            product_name= 'Bubur Ayam',
            restaurant= 'RM Palu',
            price= 10000,
            description= 'Terbuat dari nasi piihan',
            category= 'Indonesian'
        )
        response = self.client.post(reverse('products:edit_product', args=[product.id]), {
            'product_name': 'Bubur Ayam',
            'restaurant': 'RM Palu',
            'price': 15000,
            'description': 'Terbuat dari nasi kualitas terbaik',
            'category': 'Indonesian'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        product = Product.objects.create(
            user=self.user,
            product_name= 'Bubur Ayam',
            restaurant= 'RM Palu',
            price= 10000,
            description= 'Terbuat dari nasi piihan',
            category= 'Indonesian'
        )
        response = self.client.post(reverse('products:delete_product', args=[product.id]))
        self.assertEqual(response.status_code, 200)

    def test_my_products_with_products(self):
        response = self.client.get(self.my_products_url)

        self.assertEqual(response.status_code, 200)
