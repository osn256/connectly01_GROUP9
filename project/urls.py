from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:pk>/', post_views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:pk>/', post_views.UnfollowUserView.as_view(), name='unfollow_user'),
    path('accounts/', include('allauth.urls')),  # Added for allauth
    path('', post_views.home, name='home'),  # Root URL
]