"""from django.contrib import admin  # Import admin module
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]"""

"""from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', include('posts.urls')),  # Assuming you have a register view in posts.urls
]"""

"""from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('api/posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),
    path('api/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('api/comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('api/comments/<int:pk>/like/', views.LikeCommentView.as_view(), name='like_comment'),
    path('api/comments/<int:pk>/unlike/', views.UnlikeCommentView.as_view(), name='unlike_comment'),
    path('api/users/', views.UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('api/admin-only/', views.AdminOnlyView.as_view(), name='admin_only'),
    path('', include(router.urls)),
    path('posts/', include('posts.urls')),

]"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from posts import views as post_views
from . import views as project_views  # Import views from the current directory
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', project_views.UserViewSet)
router.register(r'posts', project_views.PostViewSet)
router.register(r'comments', project_views.CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', post_views.register, name='register'),
    path('home/', post_views.home, name='home'),
    path('main/', post_views.main_app, name='main_app'),
    path('profile/', project_views.profileView, name='profile'),
    path('api/', include(router.urls)),
    path('posts/', include('posts.urls')),
    path('follow/<int:pk>/', post_views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:pk>/', post_views.UnfollowUserView.as_view(), name='unfollow_user'),
]