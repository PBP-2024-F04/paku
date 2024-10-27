from django.test import TestCase
from django.urls import reverse
from .models import Product, Review
from accounts.models import User

class ReviewTests(TestCase):

    def setUp(self):
        # Create a user and product for the tests
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            user=self.user,
            product_name='Test Product',
            restaurant='Test Restaurant',
            price=10000,
            description='Test Description',
            category='Test Category'
        )
        self.client.login(username='testuser', password='password')

    def test_create_review(self):
        response = self.client.post(reverse('reviews:create_review', args=[self.product.id]), {
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 200)  # Adjust if necessary

    def test_delete_review(self):
        # Create a review to delete
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!'
        )
        response = self.client.delete(reverse('reviews:delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after deletion

    def test_edit_review(self):
        # Create a review to edit
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!'
        )
        response = self.client.post(reverse('reviews:edit_review', args=[review.id]), {
            'rating': 4,
            'comment': 'Good product!'
        })
        self.assertEqual(response.status_code, 200)  # Adjust if necessary
