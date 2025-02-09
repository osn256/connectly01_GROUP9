#CODE(90)
from django.contrib import admin
from .models import User, Post, Comment, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
# this code will reflect directly to the actual ADMIN GUI
#_____________________________________________________________added for admin access views
