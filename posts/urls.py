from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import CustomTokenObtainPairView  # Import your custom view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from django.conf.urls.static import static
from .views import add_comment
from .views import CreateCommentView, CommentListCreateView
from .views import create_comment, like_comment, unlike_comment, list_comments
from .views import LikeCommentView, UnlikeCommentView
from .views import FollowUserView, UnfollowUserView
from .views import AdminOnlyView
from .views import LikePostView, UnlikePostView
from .views import CommentListCreateView, CommentDetailView 
from .views import UserListCreateView, UserDetailView
from .views import PostListCreateView, PostDetailView
from .views import CustomTokenObtainPairView
from .views import add_comment
from .views import create_comment
from .views import like_post, delete_post
from .views import UnlikeListCreateView, UnlikeDetailView

urlpatterns = [
    # this is for all url related to authentications
    path('register/', views.register, name='register'),                                         #ADDED 2 5 2025_ 7:30 PM
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home, name='home'),                                                          #ADDED 2 5 2025_ 7:30 PM
    path('profile/', views.profile_view, name='profile'),
    path('news_feed/', views.news_feed_view, name='news_feed'),

    # this is for all url related to API
    path('api/users/', views.UserListCreateView.as_view(), name='user_list_create'),            #ADDED 2 8 2025_ 7:40 PM
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    # this is for all url related to posts 
    path('api/posts/create/', views.PostListCreateView.as_view(), name='post_list_create'),     #ADDED 2 8 2025_ 7:40 PM
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('api/posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),

    # this is for all url related to comments
    path('api/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),   #ADDED 2 8 2025_ 7:40 PM
    path('api/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('api/comments/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    path('api/comments/<int:pk>/unlike/', views.UnlikeCommentView.as_view(), name='unlike_comment'),

    # this is for Follow and Unfollow Views
    path('api/follow/<int:pk>/', views.FollowUserView.as_view(), name='follow_user'),
    path('api/unfollow/<int:pk>/', views.UnfollowUserView.as_view(), name='unfollow_user'),

    # this is for Admin Only View
    path('api/admin/', views.AdminOnlyView.as_view(), name='admin_only'),

    # this is for JWT Authentication
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    
    # this is for actual comments,posts,likes,unlikes and other views
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    path('posts/create/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='like-post'),
    #path('posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike-post'),
    
    path('posts/<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:pk>/comments/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/comments/<int:comment_id>/like/', views.LikeCommentView.as_view(), name='like-comment'),
    path('posts/<int:pk>/comments/<int:comment_id>/unlike/', views.UnlikeCommentView.as_view(), name='unlike-comment'),
    
    #path('posts/<int:id>/delete', DeletePostView.as_view(), name='delete_post'),
    #path('posts/<int:id>', GetPostView.as_view(), name='get_post'),

    path('like/<int:post_id>/', like_post, name='like_post'),                           # ADDED 3 9 2025_ 2:16 am
    path('comment/<int:post_id>/', add_comment, name='add_comment'),                    # ADDED 3 9 2025_ 2:16 am
    path('comment/create/<int:post_id>/', create_comment, name='comment_create'),
     
    path('comments/create/<int:post_id>/', create_comment, name='create_comment'),
    path('comments/like/<int:comment_id>/', like_comment, name='like_comment'),
    path('comments/unlike/<int:comment_id>/', unlike_comment, name='unlike_comment'),
    path('comments/list/<int:post_id>/', list_comments, name='list_comments'),

    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),                #ADDED 3 9 2025_ 2:16 am

    path('posts/<int:post_id>/comments/', CreateCommentView.as_view(), name='create_comment'),
    path('posts/<int:post_id>/comments/list/', CommentListCreateView.as_view(), name='comment_list'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/', views.get_post, name='get_post'),                      #ADDED 3 22 2025_ 6:29 PM
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    #path('posts/<int:post_id>/', views.get_post, name='get_post'),
    #path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('unlikes/<int:comment_id>/', unlike_comment, name='unlike_comment'),           #ADDED 3 20 2025_ 5:48pm
    path('unlike/<int:comment_id>/', unlike_comment, name='unlike_comment'),   
    path('unlikes/', UnlikeListCreateView.as_view(), name='unlike-list-create'),
    path('unlikes/<int:pk>/', UnlikeDetailView.as_view(), name='unlike-detail'),
    # Cache management URLs
    path('clear_cache/', views.clear_cache, name='clear_cache'),                        #ADDED 3 10 2025_ 10:148 am
    path('delete_cache_key/<str:key>/', views.delete_cache_key, name='delete_cache_key'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#_____________________________________________________________________________________________________________________
