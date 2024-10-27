from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from timeline.models import Post

class MyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="temp", password="HelloWorld123", email="temp@gmail.com")
        self.post = Post.objects.create(user=self.user, text="hello")

class Main(MyTestCase):
    def test_main_require_login(self):
        response = self.client.get(reverse('timeline:main'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/timeline/')

    def test_main_no_redirect_if_login(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:main'), follow=True)
        self.assertEqual(response.status_code, 200) # 200 artinya ga redirect

    def test_main_posts_exist(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:main'), follow=True)
        self.assertEqual(len(response.context['posts']), 1)

class CreatePost(MyTestCase):
    def test_create_post_require_login(self):
        response = self.client.get(reverse('timeline:create_post'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/timeline/post/')

    def test_create_post_no_redirect_if_login(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:create_post'), follow=True)
        self.assertEqual(response.status_code, 200) # 200 artinya ga redirect

    def test_create_post(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.post(reverse('timeline:create_post'), data={"text": "Hello, World"}, follow=True)
        self.assertEqual(response.status_code, 200)
        posts = Post.objects.count()
        self.assertGreater(posts, 1)

    def test_create_post_form_exist(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:create_post'), follow=True)
        self.assertIsNotNone(response.context['form'])

class ViewPost(MyTestCase):
    def test_view_post_require_login(self):
        # response = self.client.get(f'/timeline/post/{self.post.id}', follow=True)
        response = self.client.get(reverse('timeline:view_post', args=(self.post.id,)), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/timeline/post/{self.post.id}')

    def test_view_post_no_redirect_if_login(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:view_post', args=(self.post.id,)), follow=True)
        self.assertEqual(response.status_code, 200) # 200 artinya ga redirect

class EditPost(MyTestCase):
    def test_edit_post_require_login(self):
        response = self.client.get(reverse('timeline:edit_post', args=(self.post.id,)), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next=/timeline/post/{self.post.id}/edit')

    def test_edit_post_no_redirect_if_login(self):
        self.client.login(username="temp", password="HelloWorld123")
        response = self.client.get(reverse('timeline:edit_post', args=(self.post.id,)), follow=True)
        self.assertEqual(response.status_code, 200) # 200 artinya ga redirect
