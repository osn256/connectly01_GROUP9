"""from getpass import getuser
from django.shortcuts import render

def profileView(request):
    users = getuser()
    return render(request, 'profile.html', {'user': users})

"""
from rest_framework import viewsets
from posts.models import User, Post, Comment
from posts.serializers import UserSerializer, PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer