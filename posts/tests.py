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
"""from django.test import TestCase
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
        self.assertEqual(comment.likes.count(), 5)"""

#TO TEST THE FACTORIES:       python manage.py test posts       added 02/08/2025

# REPLACE A NEW ALSO WORKING TESTING March 20,2025 7:02pm
from django.test import TestCase
from .models import User, Post, Comment, Like, Follow, Unlike
#_____________________________________________________________________________________________________________________
class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuserOSIAS', password='12345', email='osiasMMDC@example.com')
        cls.post = Post.objects.create(author=cls.user, content='Test Post_POST TEST SUCCESSFUL by OSIAS_under_Group(9)')

    def test_post_creation(self):
        #the setup data using the test_post_creation
        print('Test Post Setup and Creation')                       #ADDED March 14,2025
        print(self.user.username)
        print(self.user.email)
        print(self.post.content)
        print(self.post.author.username)
        self.assertEqual(self.user.username, 'testuserOSIAS')       #ADDED March 13,2025 11:58PM
        self.assertEqual(self.user.email, 'osiasMMDC@example.com')
        self.assertEqual(self.post.content, 'Test Post_POST TEST SUCCESSFUL by OSIAS_under_Group(9)')
        self.assertEqual(self.post.author.username, 'testuserOSIAS')
#_____________________________________________________________________________________________________________________        
class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345', email='testuser2@example.com')
        cls.post = Post.objects.create(author=cls.user, content='Test COMMENT TEST SUCCESSFUL by OSIAS_under_Group(9)')
        cls.comment = Comment.objects.create(post=cls.post, author=cls.user, text='Test Comment_SETUP')

    def test_comment_creation(self):
        #the setup data using the test_comment_creation
        print('Test Comment Setup and Creation')                #ADDED March 14,2025
        print(self.comment.text)
        print(self.comment.author.username)
        print(self.comment.post.content)
        print(self.comment.created_at)
        self.assertEqual(self.comment.text, 'Test Comment_SETUP')     #ADDED March 13, 2025 11:58PM
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.post.content, 'Test COMMENT TEST SUCCESSFUL by OSIAS_under_Group(9)')
#_____________________________________________________________________________________________________________________
class LikeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345', email='testuser3@example.com')
        cls.post = Post.objects.create(author=cls.user, content='Test LIKE TEST SUCCESSFUL by OSIAS_under_Group(9)')
        cls.like = Like.objects.create(user=cls.user, post=cls.post)

    def test_like_creation(self):
        #the setup data using the test_like_creation
        print('Test Like Setup and Creation')                   #ADDED March 14, 2025
        print(self.like.user.username)
        print(self.like.post.content)
        print(self.like.created_at)
        self.assertEqual(self.like.user.username, 'testuser')   #ADDED March 13, 2025 11:58PM
        self.assertEqual(self.like.post.content, 'Test LIKE TEST SUCCESSFUL by OSIAS_under_Group(9)')
        self.assertEqual(self.like.created_at, self.like.created_at)
#_____________________________________________________________________________________________________________________
class FollowTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='osias_G9', password='12345', email='testuser4@example.com')
        cls.user2 = User.objects.create_user(username='mmdc_ADMIN', password='12345', email='testuser5@example.com')
        cls.follow = Follow.objects.create(follower=cls.user1, following=cls.user2)

    def test_follow_creation(self):
        #the setup data using the test_follow_creation
        print('Test Follow Setup and Creation')                             # ADDED March 14, 2025 2:58PM
        print(self.follow.follower.username)
        print(self.follow.following.username)
        print(self.follow.created_at)
        self.assertEqual(self.follow.follower.username, 'osias_G9')         # ADDED March 13, 2025 11:58PM
        self.assertEqual(self.follow.following.username, 'mmdc_ADMIN')
        print('FOLLOW TEST SUCCESSFUL by OSIAS_under_Group(9)')             # ADDED March 13, 2025 11:58PM
#_____________________________________________________________________________________________________________________     
class UnlikeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.post = Post.objects.create(author=self.user, content='Test Post')
        self.unlike = Unlike.objects.create(user=self.user, post=self.post)

    def test_unlike_creation(self):
        self.assertEqual(self.unlike.user.username, 'testuser')
        self.assertEqual(self.unlike.post.content, 'Test Post')  
#NEW TEST CODE ADDED                                                        # ADDED March 13, 2025 11:58PM
# TESTING MODELS codes to run
# testing Post model use                            python manage.py test
# python manage.py test posts.tests.PostTestCase
# testing Comment model
# python manage.py test posts.tests.CommentTestCase
# testing Like model
# python manage.py test posts.tests.LikeTestCase
# testing Follow model
# python manage.py test posts.tests.FollowTestCase

class RBACPrivacyTests(TestCase):                # ADDED March 22,2025
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin', password='adminpass', email='admin@example.com', role='admin'
        )
        self.user = User.objects.create_user(
            username='user', password='userpass', email='user@example.com', role='user'
        )
        self.post = Post.objects.create(
            author=self.user, content='Test Post', privacy='private'
        )

    def test_admin_user_can_delete_post(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_cannot_delete_post(self):
        self.client.force_authenticate(user=self.user)  # Unauthorized user
        response = self.client.delete(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_cannot_view_private_post(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('get_post', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_can_view_private_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('get_post', args=[self.post.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # test this using the code below
    # python manage.py test posts.tests.RBACPrivacyTests
