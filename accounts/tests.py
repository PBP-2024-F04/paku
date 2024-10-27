from django.test import TestCase
from django.urls import reverse
from accounts.models import FoodieProfile, MerchantProfile
from accounts.models import User

class MyTestCase(TestCase):
    def setUp(self):
        self.foodie_user = User.objects.create_user(username="temp", password="HelloWorld123", email="temp@gmail.com")
        self.foodie_profile = FoodieProfile.objects.create(user=self.foodie_user, full_name="hello")
        self.merchant_user = User.objects.create_user(username="temp1", password="HelloWorld123", email="temp1@gmail.com", role="Merchant")
        self.merchant_profile = MerchantProfile.objects.create(user=self.merchant_user, restaurant_name="hello")

class AccountsTest(MyTestCase):
    def test_login(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_login_redirect_if_logged_in(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_register_redirect_if_logged_in(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('accounts:register'), follow=True)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_register_foodie_redirect_if_logged_in(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('accounts:register_foodie'), follow=True)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_register_merchant_redirect_if_logged_in(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('accounts:register_foodie'), follow=True)
        self.assertRedirects(response, reverse('accounts:home'))

    def test_home_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:home'), follow=True)
        self.assertRedirects(response, reverse('accounts:login') + '?next=' + reverse('accounts:home'))

    def test_home_redirects_to_merchant_home(self):
        self.client.login(username="temp1", password="HelloWorld123")
        response = self.client.get(reverse('accounts:home'), follow=True)
        self.assertTemplateUsed(response, 'home_merchant.html')

    def test_home_redirects_to_foodie_home(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('accounts:home'), follow=True)
        self.assertTemplateUsed(response, 'home_foodie.html')
