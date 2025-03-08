from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), #ADDED 2 5 2025_ 7:30 PM
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home, name='home'),                  #ADDED 2 5 2025_ 7:30 PM

    path('api/users/', views.UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('api/posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),

    path('api/comments/', views.CommentListCreateView.as_view(), name='comment_create'),
    path('api/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('api/comments/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    path('api/comments/<int:pk>/unlike/', views.UnlikeCommentView.as_view(), name='unlike_comment'),

    # Follow and Unfollow Views
    path('api/follow/<int:pk>/', views.FollowUserView.as_view(), name='follow_user'),
    path('api/unfollow/<int:pk>/', views.UnfollowUserView.as_view(), name='unfollow_user'),

    # Admin Only View
    path('api/admin/', views.AdminOnlyView.as_view(), name='admin_only'),

]