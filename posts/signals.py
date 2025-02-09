from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def post_save_post(sender, instance, created, **kwargs):
    if created:
        print(f'New post created: {instance.content[:30]}') 

#_____________________________________________________________added to create signal

"""from posts.models import Post, User  
# Get the first user (assuming you have at least one user)
user = User.objects.first()
# Create a new post
post = Post.objects.create(content="This is a test post", author=user)"""

""">>> #OUTPUT
>>> # Create a new post
>>> post = Post.objects.create(content="This is a test post", author=user)"""

#______________________________________________________tested and working 02/08/2021
