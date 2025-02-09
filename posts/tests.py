#NEW TEST CODE ADDED
"""from django.test import TestCase
from .models import Post
from .factories import PostFactory, UserFactory

class PostModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(str(self.post), f"Post by {self.user.username} - {self.post.content[:30]}")  """  

#NEW TEST CODE ADDED FOR TESTING FACTORIES
from django.test import TestCase
from .models import User, Post, Comment, Follow
from .factories import UserFactory, PostFactory, CommentFactory, FollowFactory

class FactoryTestCase(TestCase):

    def test_user_factory(self):
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertTrue(user.username)
        self.assertTrue(user.email)
        self.assertTrue(user.check_password('password123'))

    def test_post_factory(self):
        post = PostFactory()
        self.assertIsInstance(post, Post)
        self.assertTrue(post.content)
        self.assertIsInstance(post.author, User)
        self.assertTrue(post.created_at)

    def test_comment_factory(self):
        comment = CommentFactory()
        self.assertIsInstance(comment, Comment)
        self.assertTrue(comment.text)
        self.assertIsInstance(comment.author, User)
        self.assertIsInstance(comment.post, Post)
        self.assertTrue(comment.created_at)

    def test_follow_factory(self):
        follow = FollowFactory()
        self.assertIsInstance(follow, Follow)
        self.assertIsInstance(follow.follower, User)
        self.assertIsInstance(follow.following, User)
        self.assertTrue(follow.created_at)

    def test_post_likes(self):
        post = PostFactory()
        users = UserFactory.create_batch(5)
        post.likes.add(*users)
        self.assertEqual(post.likes.count(), 5)

    def test_comment_likes(self):
        comment = CommentFactory()
        users = UserFactory.create_batch(5)
        comment.likes.add(*users)
        self.assertEqual(comment.likes.count(), 5)

#TO TEST THE FACTORIES:       python manage.py test posts       added 02/08/2025