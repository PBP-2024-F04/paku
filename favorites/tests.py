from django.urls import reverse
from django.test import TestCase
from .models import User, Favorite, Product
import uuid

class UserTestCase(TestCase):
    def setUp(self):
        self.foodie_user = User.objects.create_user(
            username="testfoodie", 
            password="pass1234", 
            role=User.Role.FOODIE
        )
        
        self.merchant_user = User.objects.create_user(
            username="testmerchant", 
            password="pass1234", 
            role=User.Role.MERCHANT
        )
        
        self.product = Product.objects.create(
            user=self.merchant_user,
            id=uuid.uuid4(),
            product_name="Test Product",
            restaurant="Test Restaurant",
            price=10000,
            description="Kuliner yang menggugang selera",
            category="Indonesian"
        )
        
        self.favorite = Favorite.objects.create(
            foodie=self.foodie_user,
            product=self.product,
            category=Favorite.Category.WANT_TO_TRY
        )

class MainFavoritesView(UserTestCase):
    def test_main_require_login(self):
        response = self.client.get(reverse('favorites:main'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/favorites/')

    def test_main_no_redirect_if_login(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:main'), follow=True)
        self.assertEqual(response.status_code, 200) 

    def test_main_favorites_exist(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:main'), follow=True)
        self.assertEqual(len(response.context['want_to_try']), 1) 

class CreateFavoriteView(UserTestCase):
    def test_create_favorite_require_login(self):
        response = self.client.get(reverse('favorites:create_favorite', args=(self.product.id,)), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/favorites/create/{self.product.id}/')

    def test_create_favorite_no_redirect_if_login(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:create_favorite', args=(self.product.id,)), follow=True)
        self.assertEqual(response.status_code, 200) 

    def test_create_favorite(self):
        self.client.login(username="testfoodie", password="pass1234")

        initial_favorites_count = Favorite.objects.count()

        response = self.client.post(reverse('favorites:create_favorite', args=(self.product.id,)), 
                                    data={"category": Favorite.Category.WANT_TO_TRY}, follow=True)
        self.assertEqual(response.status_code, 200)

        favorites_count = Favorite.objects.count()

        if initial_favorites_count > 0:
            self.assertEqual(favorites_count, initial_favorites_count) 
        else:
            self.assertEqual(favorites_count, initial_favorites_count + 1) 

    def test_create_favorite_form_exists(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:create_favorite', args=(self.product.id,)), follow=True)
        self.assertIsNotNone(response.context['form'])

class EditFavoriteView(UserTestCase):
    def test_edit_favorite_require_login(self):
        response = self.client.get(reverse('favorites:edit_favorite', args=(self.favorite.favorite_id,)), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/favorites/{self.favorite.favorite_id}/edit')

    def test_edit_favorite_no_redirect_if_login(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:edit_favorite', args=(self.favorite.favorite_id,)), follow=True)
        self.assertEqual(response.status_code, 200) 

    def test_edit_favorite(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.post(reverse('favorites:edit_favorite', args=(self.favorite.favorite_id,)), 
                                    data={"category": Favorite.Category.WANT_TO_TRY}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.favorite.refresh_from_db()
        self.assertEqual(self.favorite.category, Favorite.Category.WANT_TO_TRY)

class DeleteFavoriteView(UserTestCase):
    def test_delete_favorite_require_login(self):
        response = self.client.get(reverse('favorites:delete_favorite', args=(self.favorite.favorite_id,)), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/favorites/{self.favorite.favorite_id}/delete')

    def test_delete_favorite_no_redirect_if_login(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:delete_favorite', args=(self.favorite.favorite_id,)), follow=True)
        self.assertEqual(response.status_code, 200) 

    def test_delete_favorite(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.post(reverse('favorites:delete_favorite', args=(self.favorite.favorite_id,)), follow=True)
        self.assertRedirects(response, reverse('favorites:main'))
        self.assertFalse(Favorite.objects.filter(favorite_id=self.favorite.favorite_id).exists())

class CategoryFavoritesView(UserTestCase):
    def test_category_favorites(self):
        self.client.login(username="testfoodie", password="pass1234")
        response = self.client.get(reverse('favorites:category_favorites', args=('want_to_try',)))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.favorite, response.context['favorites'])

class MerchantFavoriteTests(UserTestCase):
    def test_merchant_cannot_create_favorite(self):
        self.client.login(username="testmerchant", password="pass1234")
        
        response = self.client.post(reverse('favorites:create_favorite', args=(self.product.id,)), 
                                    data={"category": Favorite.Category.WANT_TO_TRY}, follow=True)

        self.assertEqual(response.status_code, 403) 

    def test_merchant_cannot_edit_favorite(self):
        self.client.login(username="testmerchant", password="pass1234")
        
        foodie_favorite = Favorite.objects.create(
            foodie=self.foodie_user,
            product=self.product,
            category=Favorite.Category.WANT_TO_TRY
        )

        response = self.client.post(reverse('favorites:edit_favorite', args=(foodie_favorite.favorite_id,)), 
                                    data={"category": Favorite.Category.WANT_TO_TRY}, follow=True)

        self.assertEqual(response.status_code, 403) 

    def test_merchant_cannot_delete_favorite(self):
        self.client.login(username="testmerchant", password="pass1234")
        
        foodie_favorite = Favorite.objects.create(
            foodie=self.foodie_user,
            product=self.product,
            category=Favorite.Category.WANT_TO_TRY
        )

        response = self.client.post(reverse('favorites:delete_favorite', args=(foodie_favorite.favorite_id,)), follow=True)

        self.assertEqual(response.status_code, 403)