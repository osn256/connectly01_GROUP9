"""from django.urls import path                 # OLD RUNNING w/o the DELETE and UPDATE codes
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('posts/', views.get_posts, name='get_posts'),
    path('posts/create/', views.create_post, name='create_post'),
]"""

from django.urls import path                    
from .views import (
    UserListCreate, UserDetail,
    PostListCreate, PostDetail,
    CommentListCreate, CommentDetail
)

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:id>/', UserDetail.as_view(), name='user-detail'),
    
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:id>/', PostDetail.as_view(), name='post-detail'),

    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:id>/', CommentDetail.as_view(), name='comment-detail'),
]

