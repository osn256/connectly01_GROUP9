"""from django.contrib import admin
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  # User's unique username
    #profile_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)  # User's unique email
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created

    def __str__(self):
        return self.username

class Post(models.Model):
    content = models.TextField()  # The text content of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created

    def __str__(self):
        return self.content[:50]
#added 1 19 2024
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"
"""

"""# REVISED CONNECTLY MODEL:

from django.db import models
from django.contrib import admin

# ----- User Model -----
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)           # User's unique username
    email = models.EmailField(unique=True)                             # User's unique email
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='covers/', blank=True, null=True)
    bio = models.TextField(blank=True)                                 # Short bio for the user
    is_online = models.BooleanField(default=False)                     # User's online status
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)  # Friend connections
    created_at = models.DateTimeField(auto_now_add=True)               # Account creation date

    def __str__(self):
        return self.username


# ----- Post Model -----
class Post(models.Model):
    content = models.TextField()                                       # The text content of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)         # The user who created the post
    media = models.FileField(upload_to='posts/', blank=True, null=True)  # Media attachments (image/video)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Likes system
    shared_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)  # Shared post reference
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()


# ----- Comment Model -----
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # Nested comments
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)  # Likes for comments
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

    def total_likes(self):
        return self.likes.count()
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# ----- User Model -----
class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# ----- Post Model -----
class Post(models.Model):
    content = models.TextField()
    media = models.ImageField(upload_to='post_media/', blank=True, null=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} - {self.content[:30]}"

    def total_likes(self):
        return self.likes.count()

# ----- Comment Model -----
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"

    def total_likes(self):
        return self.likes.count()

# ----- Like Model -----
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

# ----- Follow Model -----
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"