# Core Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.views import View

from django.core.cache import cache
from django.core.exceptions import PermissionDenied

# REST framework imports
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Models and serializers
from .models import User, Post, Comment, Follow, Like, Unlike
from .serializers import (
    UserSerializer, 
    PostSerializer, 
    LikeSerializer, 
    CommentSerializer, 
    FollowSerializer, 
    CustomTokenObtainPairSerializer, 
    UnlikeSerializer
)

# Forms
from .forms import CustomUserCreationForm, PostForm, CommentForm

# Permissions and decorators
from .permissions import IsAuthorOrReadOnly, IsPostAuthor
from .decorators import role_required

# Utilities and logging
from .logger import SingletonLogger

#____________________________________________________________________________________________________________________________________
logger = SingletonLogger().get_logger()

#____________________________________________________________________________________________________________________________________
@login_required                                             # decorator to ensure user is logged in / from django.contrib.auth.decorators import login_required
def home(request):                                          # Function to render the home page
    posts = cache.get('home_posts')                         # ADDED 3 10 2025_ 10:08AM
    if not posts:                                           # If cache is empty                                        
        posts = Post.objects.all().order_by('-created_at')  # Get posts from the database
        cache.set('home_posts', posts, timeout=60*15)       # Cache the posts for 15 minutes 
    return render(request, 'home.html', {'posts': posts})   # Return the posts  # ADDED 3 10 2025_ 10:08AM


@login_required
def main_app(request):
    posts = cache.get('main_app_posts')
    if not posts:
        posts = Post.objects.all().order_by('-created_at')
        cache.set('main_app_posts', posts, timeout=60*15)  # ADDED 3 10 2025_ 10:08AM 
    return render(request, 'base.html', {'posts': posts})

@login_required
def profile_view(request):
    user = request.user
    cache_key = f'profile_view_{user.id}'                  # ADDED 3 10 2025_ 10:08AM 

    context = cache.get(cache_key)
    if not context:
        posts = Post.objects.filter(author=user).order_by('-created_at')
        followers = Follow.objects.filter(following=user)
        following = Follow.objects.filter(follower=user)
        context = {
            'user': user,
            'posts': posts,
            'followers': followers,
            'following': following,
        }
        cache.set(cache_key, context, timeout=60*15)   

    return render(request, 'profile.html', context)
    
@login_required
def news_feed_view(request):
    user = request.user
    cache_key = f'news_feed_view_{user.id}'
    context = cache.get(cache_key)                          # ADDED 3 10 2025_ 10:08AM 

    if not context:
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        context = {
            'posts': posts,
        }
        cache.set(cache_key, context, timeout=60*15)   
    return render(request, 'news_feed.html', context)

def clear_cache(request):                                   # ADDED 3 10 2025_ 10:40AM 
    cache.clear()
    return HttpResponse("Cache cleared")

def delete_cache_key(request, key):
    cache.delete(key)
    return HttpResponse(f"Cache key '{key}' deleted")       # ADDED 3 10 2025_ 10:40AM 


#____________________________________________________________________________________________________________________________________
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#____________________________________________________________________________________________________________________________________
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
#____________________________________________________________________________________________________________________________________
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

#____________________________________________________________________________________________________________________________________
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
#____________________________________________________________________________________________________________________________________
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenObtainPairView):
    pass
#____________________________________________________________________________________________________________________________________
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(f'User updated: {user.username}')

    def perform_destroy(self, instance):
        logger.info(f'User deleted: {instance.username}')
        instance.delete()
#____________________________________________________________________________________________________________________________________
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
#____________________________________________________________________________________________________________________________________
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user_to_follow = get_object_or_404(User, pk=pk)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if created:
            logger.info(f'{request.user.username} followed {user_to_follow.username}')
            return Response({"status": "followed"}, status=status.HTTP_200_OK)
        return Response({"status": "already following"}, status=status.HTTP_400_BAD_REQUEST)
#____________________________________________________________________________________________________________________________________
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
#____________________________________________________________________________________________________________________________________
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #parser_classes = [MultiPartParser, FormParser]                 #added 2 24 2025_ 7:20 PM
    parser_classes = [JSONParser, MultiPartParser, FormParser]      #added 2 27 2025_ 10:33 PM
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        logger.info(f'Post created by {post.author.username}: {post.content[:30]}')
        cache.clear()  # Clear the cache when a post is created
#____________________________________________________________________________________________________________________________________
#@method_decorator(cache_page(60 * 15), name='dispatch')           # ADDED 3 10 2025_ 10:08AM     other method to cache
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        post = serializer.save()
        logger.info(f'Post updated by {post.author.username}: {post.content[:30]}')
        cache.clear()  # Clear the cache when a post is created

    def perform_destroy(self, instance):
        logger.info(f'Post deleted by {instance.author.username}: {instance.content[:30]}')
        instance.delete()
        cache.clear()  # Clear the cache when a post is created
#____________________________________________________________________________________________________________________________________
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
#____________________________________________________________________________________________________________________________________
class LikePostView(APIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.likes.add(request.user)
        post.save()
        logger.info(f'Post liked by {request.user.username}: {post.content[:30]}')
        return Response({"status": "liked"}, status=status.HTTP_200_OK)
#____________________________________________________________________________________________________________________________________
class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.likes.remove(request.user)
        post.save()
        logger.info(f'Post unliked by {request.user.username}: {post.content[:30]}')
        return Response({"status": "unliked"}, status=status.HTTP_200_OK)
#____________________________________________________________________________________________________________________________________
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        logger.info(f'Comment created by {comment.author.username}: {comment.text[:30]}')
#____________________________________________________________________________________________________________________________________
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        comment = serializer.save()
        logger.info(f'Comment updated by {comment.author.username}: {comment.text[:30]}')

    def perform_destroy(self, instance):
        logger.info(f'Comment deleted by {instance.author.username}: {instance.text[:30]}')
        instance.delete()
#____________________________________________________________________________________________________________________________________
class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.add(request.user)
        comment.save()
        logger.info(f'Comment liked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment liked'}, status=status.HTTP_200_OK)
#____________________________________________________________________________________________________________________________________
class UnlikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        comment.likes.remove(request.user)
        comment.save()
        logger.info(f'Comment unliked by {request.user.username}: {comment.text[:30]}')
        return Response({'status': 'Comment unliked'}, status=status.HTTP_200_OK)
#____________________________________________________________________________________________________________________________________
class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(f'Admin access by {request.user.username}')
        return Response({"message": "Welcome, Admin!"})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()  # Use the custom form
    return render(request, 'register.html', {'form': form})
#____________________________________________________________________________________________________________________________________
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,IsPostAuthor] #Added March 20,2025 6:13PM

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'status': 'Post liked'}, status=status.HTTP_200_OK)
        return Response({'status': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'status': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)
#____________________________________________________________________________________________________________________________________
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] # ADDED 3 20 2025_ 6:13PM

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

#____________________________________________________________________________________________________________


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class LikePostView(generics.GenericAPIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)

class LikeCommentView(generics.GenericAPIView):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

class UnlikeCommentView(generics.GenericAPIView):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)

class FollowUserView(generics.GenericAPIView):
    def post(self, request, pk):
        user_to_follow = User.objects.get(pk=pk)
        request.user.following.add(user_to_follow)
        return Response(status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    def post(self, request, pk):
        user_to_unfollow = User.objects.get(pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response(status=status.HTTP_200_OK)

class AdminOnlyView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(data={"message": "Hello, Admin!"}, status=status.HTTP_200_OK)
#____________________________________________________________________________________________________________________________________    

#class CustomTokenObtainPairView(TokenObtainPairView):
#    serializer_class = CustomTokenObtainPairSerializer

#class UserListCreateView(generics.ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [AllowAny]

#    def perform_create(self, serializer):
#        user = serializer.save()
#        logger.info(f'User created: {user.username}')


#____________________________________________________________________________________________________________________________________

@method_decorator(login_required, name='dispatch')
class PostListCreateView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        post_form = PostForm()
        comment_form = CommentForm()
        return render(request, 'posts/home.html', {'posts': posts, 'post_form': post_form, 'comment_form': comment_form})

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': post.id,
                    'content': post.content,
                    'media_url': post.media.url if post.media else '',
                    'author': post.author.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                })
            return redirect('home')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid form data'}, status=400)
        return render(request, 'posts/home.html', {'post_form': post_form})

"""@login_required
@role_required(allowed_roles=['admin'])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'})
    return JsonResponse({'error': 'Unauthorized'}, status=401)

@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.privacy == 'private' and post.author != request.user:
        raise PermissionDenied
    return JsonResponse({'content': post.content})"""

@api_view(['DELETE'])                                # UPDATED March 22,2025 for RBAC and Privacy Testing // WORKING CODE
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if request.user.role == 'admin' or post.author == request.user:
            post.delete()
            return Response({'message': 'Post deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])                                  # UPDATED March 22,2025 for RBAC and Privacy Testing // WORKING CODE
@permission_classes([IsAuthenticated])
def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.privacy == 'private' and post.author != request.user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'content': post.content}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


@login_required
@csrf_exempt
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'id': post_id, 'likes_count': post.likes.count(), 'liked': liked})

@login_required
@csrf_exempt
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.unlikes.all():
        post.unlikes.remove(request.user)
        unliked = False
    else:
        post.unlikes.add(request.user)
        unliked = True

    return JsonResponse({'id': post_id, 'unlikes_count': post.unlikes.count(), 'unliked': unliked})

@login_required
@csrf_exempt
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return JsonResponse({'id': comment_id, 'likes_count': comment.likes.count(), 'liked': liked})

@login_required
@csrf_exempt
def unlike_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user in comment.unlikes.all():
        comment.unlikes.remove(request.user)
        unliked = False
    else:
        comment.unlikes.add(request.user)
        unliked = True

    return JsonResponse({'id': comment_id, 'unlikes_count': comment.unlikes.count(), 'unliked': unliked})
#____________________________________________________________________________________________________________________________________   

class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
@login_required
@csrf_exempt
def add_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )
            return JsonResponse({
                'id': comment.id,
                'author': comment.author.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%B %d, %Y %I:%M %p'),
                'likes_count': comment.likes.count()
            })
        return JsonResponse({'error': 'Empty comment'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.data.get('text')
    parent_id = request.data.get('parent_id')

    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)
    
    # Create the comment
    comment = Comment.objects.create(
        text=text,
        author=request.user,
        post=post,
        parent=parent
    )

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': comment.total_likes()
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)

    return JsonResponse({
        'liked': False,
        'likes_count': comment.total_likes()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None).order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

#____________________________________________________________________________________________________________________________________
@method_decorator(login_required, name='dispatch')
class CommentListCreateView(View):
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': comment.id,
                    'text': comment.text,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                })
            return redirect('home')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)

        return render(request, 'posts/home.html', {'form': form})

#____________________________________________________________________________________________________________________________________   
class UnlikeListCreateView(generics.ListCreateAPIView):     #ADDED March 20, 2025 5:46pm
    queryset = Unlike.objects.all()
    serializer_class = UnlikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#____________________________________________________________________________________________________________________________________
class UnlikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Unlike.objects.all()
    serializer_class = UnlikeSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.unlikes.all():
        comment.unlikes.remove(user)
        unliked = False
    else:
        comment.unlikes.add(user)
        unliked = True

    return JsonResponse({
        'unliked': unliked,
        'unlikes_count': comment.total_unlikes()
    })
"""from django.shortcuts import render, redirect, get_object_or_404
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
        return Response({'status': 'Comment unliked'}, status=status.HTTP_200_OK)"""
