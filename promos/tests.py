from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import Promo
from accounts.models import User, MerchantProfile

class PromoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.merchant_user = User.objects.create_user(
            username="merchant",
            password="HelloWorld123",
            role='Merchant'
        )
        self.merchant_profile = MerchantProfile.objects.create(
            user=self.merchant_user,
            restaurant_name="Merchant Restaurant"
        )
        self.promo = Promo.objects.create(
            user=self.merchant_user,
            promo_title="Promo 12.12",
            promo_description="Beli 12 porsi diskon 12%",
            batas_penggunaan=timezone.datetime(2024, 12, 12).date()
        )

    def test_main_url_exists(self):
        response = self.client.get(reverse('promos:main'))
        self.assertEqual(response.status_code, 200)

    def test_main_uses_main_template(self):
        response = self.client.get(reverse('promos:main'))
        self.assertTemplateUsed(response, 'promos.html')

    def test_my_promos_url_exists(self):
        self.client.login(username="merchant", password="HelloWorld123")
        response = self.client.get(reverse('promos:my_promos'))
        self.assertEqual(response.status_code, 200)

    def test_my_promos_uses_my_promos_template(self):
        self.client.login(username="merchant", password="HelloWorld123")
        response = self.client.get(reverse('promos:my_promos'))
        self.assertTemplateUsed(response, 'my_promos.html')

    def test_create_promo(self):
        self.client.login(username="merchant", password="HelloWorld123")
        self.client.post(reverse('promos:add_promo'), {
            'promo_title': "Promo 12.12",
            'promo_description': "Beli 12 porsi diskon 12%",
            'batas_penggunaan': timezone.datetime(2024, 12, 12).date()
        })
        self.assertTrue(Promo.objects.filter(promo_title="Promo 12.12").exists())

    def test_update_promo(self):
        self.client.login(username="merchant", password="HelloWorld123")
        self.client.post(reverse('promos:update_promo', args=[self.promo.id]), {
            'promo_title': "Updated Promo 12.12",
            'promo_description': "This promo has been updated",
            'batas_penggunaan': timezone.datetime(2024, 12, 12).date()
        })
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.promo_title, "Updated Promo 12.12")

    def test_delete_promo(self):
        self.client.login(username="merchant", password="HelloWorld123")
        self.client.post(reverse('promos:delete_promo', args=[self.promo.id]))
        self.assertFalse(Promo.objects.filter(id=self.promo.id).exists())
