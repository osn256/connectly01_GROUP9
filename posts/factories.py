import factory
from .models import User, Post, Comment, Follow

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    content = factory.Faker('text', max_nb_chars=200)
    media = None
    author = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time')

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.likes.add(user)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('text', max_nb_chars=200)
    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    parent = None
    created_at = factory.Faker('date_time')

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.likes.add(user)

class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow
    follower = factory.SubFactory(UserFactory)
    following = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time')

#_____________________________________________________________added for admin access views