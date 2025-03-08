from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from posts.models import User, Post, Comment, Follow
from posts.serializers import UserSerializer, PostSerializer, CommentSerializer, FollowSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

def profileView(request):
    users = User.objects.all()
    return render(request, 'profile.html', {'users': users})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            return Response({"status": "followed"}, status=status.HTTP_200_OK)
        return Response({"status": "already following"}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
        if follow:
            follow.delete()
            return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)
        return Response({"status": "not following"}, status=status.HTTP_400_BAD_REQUEST)
    
