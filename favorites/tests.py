from django.test import TestCase
from django.contrib.auth import get_user_model
from favorites.models import Favorite
from products.models import Product
import uuid

User = get_user_model()

class FavoriteModelTests(TestCase):
    def setUp(self):
        # Create a test user with the 'Foodie' role
        self.user = User.objects.create_user(username="testuser", password="testpass", role="Foodie")
        
        # Create a product with all required fields
        self.product = Product.objects.create(
            product_name="Test Product",
            restaurant="Test Restaurant",
            price=100,
            description="A delicious test product",
            category="Test Category"
        )
        
        # Create an initial Favorite instance
        self.favorite = Favorite.objects.create(
            foodie=self.user,
            product=self.product,
            category=Favorite.Category.WANT_TO_TRY
        )

    def test_favorite_creation(self):
        """Test if a favorite is created successfully"""
        favorite = Favorite.objects.create(
            foodie=self.user,
            product=self.product,
            category=Favorite.Category.WANT_TO_TRY
        )
        self.assertIsNotNone(favorite.favorite_id)
        self.assertEqual(favorite.foodie, self.user)
        self.assertEqual(favorite.product, self.product)
        self.assertEqual(favorite.category, Favorite.Category.WANT_TO_TRY)

    def test_favorite_edit(self):
        """Test if the favorite can be edited successfully"""
        self.favorite.category = Favorite.Category.ALL_TIME_FAVORITES
        self.favorite.save()
        
        # Refresh from database to ensure changes are saved
        updated_favorite = Favorite.objects.get(pk=self.favorite.favorite_id)
        self.assertEqual(updated_favorite.category, Favorite.Category.ALL_TIME_FAVORITES)

    def test_favorite_deletion(self):
        """Test if the favorite can be deleted successfully"""
        favorite_id = self.favorite.favorite_id
        self.favorite.delete()
        
        with self.assertRaises(Favorite.DoesNotExist):
            Favorite.objects.get(pk=favorite_id)
            
    def test_duplicate_favorite(self):
        """Test that a user cannot add the same product to favorites multiple times"""
        with self.assertRaises(Exception):
            Favorite.objects.create(
                foodie=self.user,
                product=self.product,
                category=Favorite.Category.FAVORITE
            )

    def test_product_association(self):
        """Test that the favorite is correctly associated with the product"""
        self.assertEqual(self.favorite.product.product_name, "Test Product")
        self.assertEqual(self.favorite.product.restaurant, "Test Restaurant")
        self.assertEqual(self.favorite.product.price, 100)

    def test_user_association(self):
        """Test that the favorite is correctly associated with the user"""
        self.assertEqual(self.favorite.foodie.username, "testuser")
        self.assertTrue(self.favorite.foodie.check_password("testpass"))
