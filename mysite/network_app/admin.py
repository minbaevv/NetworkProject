from django.contrib import admin
from .models import (
    UserProfile, Content, Post, SavePostItem, SavePost,
    PostLike, Stories, Hashtag, Follow, CommentLike
)


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ContentInline, PostLikeInline]



class SavePostItemInline(admin.TabularInline):
    model = SavePostItem
    extra = 1


@admin.register(SavePost)
class SavePostAdmin(admin.ModelAdmin):
    inlines = [SavePostItemInline]


class StoriesInline(admin.TabularInline):
    model = Stories
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [StoriesInline]



admin.site.register(Hashtag)
admin.site.register(Follow)
admin.site.register(CommentLike)
