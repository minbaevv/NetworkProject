from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    user_image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user_network = models.URLField(null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile,related_name='followers',on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile,related_name='following',on_delete=models.CASCADE)
    class Meta:
        unique_together = ('follower', 'following')
    def __str__(self):
        return f'{self.follower} -> {self.following}'


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'#{self.hashtag_name}'


class Post(models.Model):
    author = models.ForeignKey(UserProfile,related_name='posts',on_delete=models.CASCADE)
    music = models.FileField(upload_to='music/', null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    description = models.TextField(null=True, blank=True)
    people = models.ManyToManyField(UserProfile, related_name='tagged_posts', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.id} by {self.author}'


class Content(models.Model):
    post = models.ForeignKey(Post,related_name='contents',on_delete=models.CASCADE)
    file = models.FileField(upload_to='posts/')

    def __str__(self):
        return f'Content for post {self.post.id}'


class PostLike(models.Model):
    user = models.ForeignKey(
        UserProfile,
        related_name='post_likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} liked post {self.post.id}'


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,related_name='comments',on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on post {self.post.id}'


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment,related_name='likes',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,related_name='comment_likes',on_delete=models.CASCADE)
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} liked comment {self.comment.id}'


class SavePost(models.Model):
    user = models.ForeignKey(UserProfile,related_name='saved_posts',on_delete=models.CASCADE)
    def __str__(self):
        return f'Saved posts of {self.user}'


class SavePostItem(models.Model):
    save_post = models.ForeignKey(SavePost,related_name='items',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='saved_in',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('save_post', 'post')
    def __str__(self):
        return f'Post {self.post.id} saved'


class Stories(models.Model):
    user = models.ForeignKey(UserProfile,related_name='stories',on_delete=models.CASCADE)
    file = models.FileField(upload_to='stories/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story by {self.user}'

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)