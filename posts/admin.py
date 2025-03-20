"""#CODE(90)
from django.contrib import admin
from .models import User, Post, Comment, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
# this code will reflect directly to the actual ADMIN GUI
#_____________________________________________________________added for admin access views"""

from django.contrib import admin                                #added 2_10_2025
from .models import User, Post, Comment, Follow, Like, Unlike
#_____________________________________________________________________________________________________________________
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'is_active', 'is_staff', 'last_login', 'is_superuser')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users']
    actions_on_top = True
    actions_on_bottom = False
    date_hierarchy = 'date_joined'
    actions_selection_counter = True
    list_display_links = ('id', 'username')
    list_editable = ('is_active', 'is_staff', 'is_superuser')
    list_per_page = 15
    list_max_show_all = 100
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    
#_____________________________________________________________________________________________________________________
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('author', 'created_at')
    ordering = ('-created_at',)
    list_display_links = ('id', 'content')
 
    list_per_page = 15
    list_max_show_all = 100
    date_hierarchy = 'created_at'
    actions = ['delete_selected', 'make_published', 'make_draft', 'make_review', 'make_private', 'make_public',]
    actions_on_top = True
    actions_on_bottom = False
#_____________________________________________________________________________________________________________________
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_at')
    search_fields = ('author__username', 'post__content', 'text')
    list_filter = ('author', 'post', 'created_at')
#_____________________________________________________________________________________________________________________
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)
#_____________________________________________________________________________________________________________________
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    search_fields = ('user__username', 'post__content')
    list_filter = ('created_at',)
#_____________________________________________________________________________________________________________________
@admin.register(Unlike)
class UnlikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    search_fields = ('user__username', 'post__content')
    list_filter = ('created_at',)
