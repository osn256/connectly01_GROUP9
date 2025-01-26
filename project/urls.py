from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
    path('posts/', include('posts.urls')),
    path('api/', include('posts.urls')),                # added because of 404 Error 1-25-2025
]