"""from django.urls import path
from .views import UserListCreate, PostListCreate, CommentListCreate

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
]"""

"""from django.urls import path                    
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
"""
"""from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('api/users/', views.UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('api/posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),

    path('api/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('api/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('api/comments/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    path('api/comments/<int:pk>/unlike/', views.UnlikeCommentView.as_view(), name='unlike_comment'),

    # Admin Only View
    path('api/admin/', views.AdminOnlyView.as_view(), name='admin_only'),

    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]