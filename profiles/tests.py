from django.test import TestCase
from django.urls import reverse
from accounts.models import FoodieProfile, User
from products.models import Product
from timeline.models import Post

class MyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="temp", password="HelloWorld123", email="temp@gmail.com")
        self.foodieprofile = FoodieProfile.objects.create(user=self.user, full_name="hello")
    
class Posts(MyTestCase):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(user=self.user, text="hello")
        self.product = Product.objects.create(
            user=self.user,
            product_name="Test Product",
            restaurant="Test Restaurant",
            price=10000,
            description="Kuliner yang menggugang selera",
            category="Indonesian"
        )

    def test_posts_require_login(self):
        response = self.client.get(reverse('profiles:profile_posts', args=['temp']), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/profile/@temp')

    def test_posts_no_redirect_if_login(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('profiles:profile_posts', args=['temp']), follow=True)
        self.assertEqual(response.status_code, 200) # 200 artinya ga redirect

    def test_posts_posts_exist(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('profiles:profile_posts', args=['temp']), follow=True)
        self.assertEqual(len(response.context['posts']), 1)
