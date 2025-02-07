"""from rest_framework import serializers
from .models import User, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']


    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value


# NEW SERIALIZZERS:

from rest_framework import serializers
from .models import User, Post, Comment

# ----- User Serializer -----
class UserSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)  # Show friend usernames instead of IDs

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'cover_photo', 'bio', 'is_online', 'friends', 'created_at']


# ----- Comment Serializer -----
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Display author's username
    likes_count = serializers.SerializerMethodField()  # Count likes for the comment
    replies = serializers.SerializerMethodField()      # Nested replies for comments

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'parent', 'likes_count', 'replies', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies(self, obj):
        replies = obj.replies.all()  # Fetch nested replies
        return CommentSerializer(replies, many=True).data


# ----- Post Serializer -----
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Include author details
    likes_count = serializers.SerializerMethodField()  # Count likes
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'media', 'likes_count', 'shared_from', 'comments', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
"""


from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Post, Comment, Like, Follow

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 'bio', 'is_online', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            bio=validated_data.get('bio', ''),
            is_online=validated_data.get('is_online', False),
            profile_picture=validated_data.get('profile_picture', None)
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'media', 'author', 'likes_count', 'comments', 'created_at']

    def get_likes_count(self, obj):
        return obj.total_likes()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at', 'replies']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']