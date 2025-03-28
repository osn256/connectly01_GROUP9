from django.db import models
from django.contrib.auth.models import AbstractUser

# ----- User Model -----
class User(AbstractUser):                               # Create a custom user model that extends the AbstractUser class    
    ROLE_CHOICES = (                                     # User role choices ADDED 3 10 2025 7:01PM
        ('admin', 'Admin'),
        ('user', 'User'),
        ('guest', 'Guest'),                             # see changes in the role field of the User model in Admin of the Django Admin  
    )
    email = models.EmailField(unique=True)              # User's unique email 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)   # User's profile picture
    bio = models.TextField(blank=True, null=True)                                           # User's bio
    is_online = models.BooleanField(default=False)                                          # User's online status
    created_at = models.DateTimeField(auto_now_add=True)                                    # Timestamp when the user was created
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')            # User role (admin, user, etc.)             # ADDED 3 10 2025 7:01PM
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)                  # User's friends                            # ADDED 3 10 2025 7:01PM
    is_active = models.BooleanField(default=True)                                           # User's active status                      # ADDED 3 10 2025 7:01PM
    is_staff = models.BooleanField(default=False)                                           # User's staff status                       # ADDED 3 10 2025 7:01PM
    is_superuser = models.BooleanField(default=False)                                       # User's superuser status                   # ADDED 3 10 2025 7:01PM
    date_joined = models.DateTimeField(auto_now_add=True)                                   # Timestamp when the user joined             # ADDED 3 10 2025 7:01PM
    last_login = models.DateTimeField(auto_now_add=True)                                    # Timestamp when the user last logged in     # ADDED 3 10 2025 7:01PM
    #to see the last_login field in the Django Admin, you need to add it to the list_display attribute of the UserAdmin class in the admin.py file.
    is_superuser = models.BooleanField(default=False)                                       # User's superuser status                   # ADDED 3 10 2025 7:01PM
    #to edit the superuser status of a user, you need to add the is_superuser field to the list_editable attribute of the UserAdmin class in the admin.py file.


    # Change the default username field to email the LOGIN_FIELD will be email
    #USERNAME_FIELD = 'email'            #ADDED 3 9 2025 1:25am
    #REQUIRED_FIELDS = ['username']      #ADDED 3 9 2025 1:25am
    
    def __str__(self):                  # String representation of the user
        return self.username            # Return the username   
    
    def total_friends(self):            # Method to get the total number of friends
         return self.friends.count()     # Return the total number of friends
    
    # to

    def total_posts(self):              # Method to get the total number of posts
        return self.posts.count()       # Return the total number of posts    

################################################### Post Model ###################################################

class Post(models.Model):                # Post model
    PRIVACY_CHOICES = (                  # Post privacy (public or private) March 20, 2025 7:20PM
        ('public', 'Public'),
        ('private', 'Private'),
    )
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')  # Post privacy (public or private) March 20, 2025 7:20PM
    content = models.TextField()         # Post content
    media = models.ImageField(upload_to='post_media/', blank=True, null=True)           # Post media (image or video)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)    # Post author
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)        # Post likes
    unlikes = models.ManyToManyField(User, related_name='unliked_posts', blank=True)    # Post unlikes
    created_at = models.DateTimeField(auto_now_add=True)                                # Timestamp when the post was created
    list_display = ('id', 'author', 'content', 'created_at')                            # List display for the PostAdmin class
    search_fields = ('author__username', 'content')                                     # Search fields for the PostAdmin class
    list_filter = ('author', 'created_at')                                              # List filter for the PostAdmin class


    def __str__(self):                                                                                       # String representation of the post    
        return f"Post by {self.author.username} - {self.content[:30]} on {self.created_at}"                  # Return the post author, content, and created_at timestamp    

    def total_likes(self):                                                              # Method to get the total likes of a post
        return self.likes.count()                                                       # Return the total number of likes for the post
    
    def total_unlikes(self):                                                            # Method to get the total unlikes of a post
        return self.unlikes.count()                                                     # Return the total number of unlikes for the post                        

    def total_comments(self):                                                           # Method to get the total comments of a post
        return self.comments.count()                                                    # Return the total number of comments for the post
   
    def __str__(self):                                                                          # String representation of the post
        return f"Post by {self.author.username} - {self.content[:30]} on {self.created_at}"     # Return the post author, content, and created_at timestamp
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
