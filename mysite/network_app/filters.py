import django_filters
from django_filters import FilterSet
from .models import Post, UserProfile, Comment, Stories, Follow


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'author__username': ['exact', 'icontains'],
            'hashtags': ['exact'],
            'hashtags__hashtag_name': ['exact', 'icontains'],
            'description': ['icontains'],
            'created_date': ['exact', 'gte', 'lte', 'gt', 'lt'],
            'people': ['exact'],
        }


class UserProfileFilter(FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'username': ['exact', 'icontains'],
            'bio': ['icontains'],
            'date_registered': ['exact', 'gte', 'lte', 'gt', 'lt'],
        }


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            'post': ['exact'],
            'user': ['exact'],
            'user__username': ['exact', 'icontains'],
            'text': ['icontains'],
            'created_date': ['exact', 'gte', 'lte', 'gt', 'lt'],
        }


class StoriesFilter(FilterSet):
    class Meta:
        model = Stories
        fields = {
            'user': ['exact'],
            'user__username': ['exact', 'icontains'],
            'created_date': ['exact', 'gte', 'lte', 'gt', 'lt'],
        }


class FollowFilter(FilterSet):
    class Meta:
        model = Follow
        fields = {
            'follower': ['exact'],
            'following': ['exact'],
            'follower__username': ['exact', 'icontains'],
            'following__username': ['exact', 'icontains'],
        }