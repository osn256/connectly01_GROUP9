from django.test import TestCase
from .models import Post
from .factories import PostFactory, UserFactory

class PostModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(str(self.post), f"Post by {self.user.username} - {self.post.content[:30]}")    