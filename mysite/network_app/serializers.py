from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (
    UserProfile, Follow, Hashtag, Post, Content,
    PostLike, Comment, CommentLike, SavePost, SavePostItem, Stories
)
from rest_framework_simplejwt.tokens import RefreshToken



class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password','first_name', 'last_name'
                )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }






class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'user_image', 'bio',
                  'user_network', 'date_registered', 'followers_count',
                  'following_count', 'posts_count']
        read_only_fields = ['date_registered']

    def get_followers_count(self, obj):
        return obj.following.count()

    def get_following_count(self, obj):
        return obj.followers.count()

    def get_posts_count(self, obj):
        return obj.posts.count()


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'hashtag_name']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'file']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'like']


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_date',
                  'likes_count', 'is_liked']
        read_only_fields = ['created_date']

    def get_likes_count(self, obj):
        return obj.likes.filter(like=True).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, like=True).exists()
        return False


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'like']


class PostListSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    contents = ContentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'music', 'hashtags', 'description',
                  'contents', 'created_date', 'likes_count', 'comments_count',
                  'is_liked', 'is_saved']
        read_only_fields = ['created_date']

    def get_likes_count(self, obj):
        return obj.likes.filter(like=True).count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, like=True).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            save_post = SavePost.objects.filter(user=request.user).first()
            if save_post:
                return SavePostItem.objects.filter(save_post=save_post, post=obj).exists()
        return False


class PostDetailSerializer(serializers.ModelSerializer):
    username = UserProfileSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    people = UserProfileSerializer(many=True, read_only=True)
    contents = ContentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'username', 'music', 'hashtags', 'description',
                  'people', 'contents', 'comments', 'created_date',
                  'likes_count', 'comments_count', 'is_liked', 'is_saved']
        read_only_fields = ['created_date']

    def get_likes_count(self, obj):
        return obj.likes.filter(like=True).count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, like=True).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            save_post = SavePost.objects.filter(user=request.user).first()
            if save_post:
                return SavePostItem.objects.filter(save_post=save_post, post=obj).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    follower = UserProfileSerializer(read_only=True)
    following = UserProfileSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']


class SavePostItemSerializer(serializers.ModelSerializer):
    post = PostListSerializer(read_only=True)

    class Meta:
        model = SavePostItem
        fields = ['id', 'post']


class SavePostSerializer(serializers.ModelSerializer):
    items = SavePostItemSerializer(many=True, read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = SavePost
        fields = ['id', 'user', 'items']


class StoriesSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Stories
        fields = ['id', 'user', 'file', 'created_date']
        read_only_fields = ['created_date']