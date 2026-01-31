from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from .models import (
    UserProfile, Follow, Hashtag, Post, Content,
    PostLike, Comment, CommentLike, SavePost, SavePostItem, Stories
)
from .serializers import (
    UserProfileSerializer, FollowSerializer, HashtagSerializer,
    PostListSerializer, PostDetailSerializer, ContentSerializer,
    PostLikeSerializer, CommentSerializer, CommentLikeSerializer,
    SavePostSerializer, SavePostItemSerializer, StoriesSerializer, UserProfileRegisterSerializer,LoginSerializer
)
from .filters import PostFilter, UserProfileFilter, CommentFilter, StoriesFilter, FollowFilter
from .pagination import (
    PostPagination, UserProfilePagination, CommentPagination,
    StoriesPagination, FollowPagination
)
from .permissions import (
    IsAuthorOrReadOnly, IsOwnerOrReadOnly,
    IsCommentAuthorOrReadOnly, IsStoryOwnerOrReadOnly
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = UserProfileFilter
    ordering_fields = ['username', 'date_registered']
    search_fields = ['username', 'bio']
    pagination_class = UserProfilePagination

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfilePostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Post.objects.filter(author_id=user_id).order_by('-created_date')


class UserFollowersAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = FollowFilter
    ordering_fields = ['id']
    search_fields = ['follower__username']

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Follow.objects.filter(following_id=user_id)


class UserFollowingAPIView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = FollowFilter
    ordering_fields = ['id']
    search_fields = ['following__username']

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Follow.objects.filter(follower_id=user_id)


class UserFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(UserProfile, pk=pk)
        if request.user == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        if created:
            return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already following'}, status=status.HTTP_200_OK)


class UserUnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user_to_unfollow = get_object_or_404(UserProfile, pk=pk)
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PostFilter
    ordering_fields = ['created_date', 'id']
    search_fields = ['description', 'author__username']
    pagination_class = PostPagination


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = PostLike.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'like': True}
        )
        if not created:
            like.like = not like.like
            like.save()

        return Response({
            'liked': like.like,
            'likes_count': post.likes.filter(like=True).count()
        })


class PostSaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        save_post, _ = SavePost.objects.get_or_create(user=request.user)
        save_item, created = SavePostItem.objects.get_or_create(
            save_post=save_post,
            post=post
        )

        if created:
            return Response({'status': 'saved'}, status=status.HTTP_201_CREATED)
        else:
            save_item.delete()
            return Response({'status': 'unsaved'}, status=status.HTTP_200_OK)


class PostCommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id).order_by('-created_date')


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all().order_by('-created_date')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CommentFilter
    ordering_fields = ['created_date', 'id']
    search_fields = ['text', 'user__username']
    pagination_class = CommentPagination


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]


class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={'like': True}
        )
        if not created:
            like.like = not like.like
            like.save()

        return Response({
            'liked': like.like,
            'likes_count': comment.likes.filter(like=True).count()
        })


class HashtagListAPIView(generics.ListAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class HashtagDetailAPIView(generics.RetrieveAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class HashtagPostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        hashtag_id = self.kwargs['pk']
        return Post.objects.filter(hashtags__id=hashtag_id).order_by('-created_date')


class SavedPostsListAPIView(generics.ListAPIView):
    serializer_class = SavePostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavePost.objects.filter(user=self.request.user)


class StoriesListAPIView(generics.ListAPIView):
    queryset = Stories.objects.all().order_by('-created_date')
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = StoriesFilter
    ordering_fields = ['created_date', 'id']
    search_fields = ['user__username']
    pagination_class = StoriesPagination


class StoriesCreateAPIView(generics.CreateAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoriesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesSerializer
    permission_classes = [IsStoryOwnerOrReadOnly]


class FollowingStoriesAPIView(generics.ListAPIView):
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StoriesPagination

    def get_queryset(self):
        following_users = self.request.user.followers.values_list('following', flat=True)
        return Stories.objects.filter(user__in=following_users).order_by('-created_date')