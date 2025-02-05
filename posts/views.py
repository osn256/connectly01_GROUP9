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

from rest_framework import generics
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAuthorOrReadOnly, IsPostAuthor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .logger import SingletonLogger

logger = SingletonLogger().get_logger()

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

class LikeCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can like comments

    def patch(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.likes.add(request.user)
        comment.save()
        logger.info(f'Comment liked by {request.user.username}: {comment.text[:30]}')
        return Response({"status": "liked"}, status=status.HTTP_200_OK)

class UnlikeCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can unlike comments

    def patch(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.likes.remove(request.user)
        comment.save()
        logger.info(f'Comment unliked by {request.user.username}: {comment.text[:30]}')
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)

# ADMIN ONLY VIEW
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(f'Admin access by {request.user.username}')
        return Response({"message": "Welcome, Admin!"})