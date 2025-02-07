# Create your views here.
#Retrieve All Users (GET):
"""
from django.http import JsonResponse
from .models import User


def get_users(request):
    try:
        users = list(User.objects.values('id', 'username', 'email', 'created_at'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#Create a User (POST):

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

#Retrieve All Posts (GET):
from .models import Post


def get_posts(request):
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#Create a Post (POST):
@csrf_exempt
def create_post(request):
    import pdb; pdb.set_trace()  # Add this breakpoint
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
"""

"""#ADDED 1 19 2025
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):                      # ADDED TO UPDATE AND DELETE SINGLE USER
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):                      # ADDED TO UPDATE AND DELETE SINGLE USER
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):                   # ADDED TO UPDATE AND DELETE SINGLE USER
    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)"""


"""from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer


# ----- User ViewSet -----
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Post ViewSet -----
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes.add(request.user)
        return Response({'status': 'Post liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.likes.remove(request.user)
        return Response({'status': 'Post unliked'})


# ----- Comment ViewSet -----
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.add(request.user)
        return Response({'status': 'Comment liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.remove(request.user)
        return Response({'status': 'Comment unliked'})
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly, IsPostAuthor
from .logger import SingletonLogger
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken

logger = SingletonLogger().get_logger()

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def main_app(request):
    return render(request, 'main_app.html')

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

@login_required
def home(request):
    return render(request, 'home.html')

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