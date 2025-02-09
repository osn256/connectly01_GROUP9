from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Post, Comment, Follow
from .serializers import UserSerializer, PostSerializer, CommentSerializer, FollowSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly, IsPostAuthor
from .logger import SingletonLogger
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken

logger = SingletonLogger().get_logger()

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def main_app(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main_app.html', {'posts': posts})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# USER VIEWS    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow any user to create a new user

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f'User created: {user.username}')

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(f'User updated: {user.username}')

    def perform_destroy(self, instance):
        logger.info(f'User deleted: {instance.username}')
        instance.delete()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            logger.info(f'{request.user.username} followed {user_to_follow.username}')
            return Response({"status": "followed"}, status=status.HTTP_200_OK)
        return Response({"status": "already following"}, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
        if follow:
            follow.delete()
            logger.info(f'{request.user.username} unfollowed {user_to_unfollow.username}')
            return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)
        return Response({"status": "not following"}, status=status.HTTP_400_BAD_REQUEST)

# POST VIEWS
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create posts

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)  # Set the author to the currently authenticated user
        logger.info(f'Post created by {post.author.username}: {post.content[:30]}')

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]  # Only the author can edit or delete

    def perform_update(self, serializer):
        post = serializer.save()
        logger.info(f'Post updated by {post.author.username}: {post.content[:30]}')

    def perform_destroy(self, instance):
        logger.info(f'Post deleted by {instance.author.username}: {instance.content[:30]}')
        instance.delete()

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.likes.add(request.user)
        post.save()
        logger.info(f'Post liked by {request.user.username}: {post.content[:30]}')
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.likes.remove(request.user)
        post.save()
        logger.info(f'Post unliked by {request.user.username}: {post.content[:30]}')
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)

# COMMENT VIEWS
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create comments

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        logger.info(f'Comment created by {comment.author.username}: {comment.text[:30]}')

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]  # Only the author can edit or delete

    def perform_update(self, serializer):
        comment = serializer.save()
        logger.info(f'Comment updated by {comment.author.username}: {comment.text[:30]}')

    def perform_destroy(self, instance):
        logger.info(f'Comment deleted by {instance.author.username}: {instance.text[:30]}')
        instance.delete()

class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.add(request.user)
        comment.save()
        logger.info(f'Comment liked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment liked'}, status=status.HTTP_200_OK)

class UnlikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.remove(request.user)
        comment.save()
        logger.info(f'Comment unliked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment unliked'}, status=status.HTTP_200_OK)

# ADMIN ONLY VIEW
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(f'Admin access by {request.user.username}')
        return Response({"message": "Welcome, Admin!"})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes.add(request.user)
        post.save()
        logger.info(f'Post liked by {request.user.username}: {post.content[:30]}')
        return Response({'status': 'Post liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes.remove(request.user)
        post.save()
        logger.info(f'Post unliked by {request.user.username}: {post.content[:30]}')
        return Response({'status': 'Post unliked'}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.add(request.user)
        comment.save()
        logger.info(f'Comment liked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.remove(request.user)
        comment.save()
        logger.info(f'Comment unliked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment unliked'}, status=status.HTTP_200_OK)