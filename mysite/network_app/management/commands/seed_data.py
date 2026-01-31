from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from network_app.models import (
    Follow, Hashtag, Post,
    PostLike, Comment, CommentLike,
    SavePost, SavePostItem, Stories
)

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed database with REALISTIC info (names, posts, comments) and fake files"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Seeding realistic data...")

        # ---------- USERS ----------
        users = []
        for _ in range(6):
            name = fake.first_name()
            surname = fake.last_name()
            username = f"{name.lower()}_{surname.lower()}"
            bio = fake.sentence(nb_words=12)
            user_network = fake.url()
            user = User.objects.create_user(
                username=username,
                password="12345678",
                bio=bio,
                user_network=user_network
            )

            # fake avatar placeholder (optional)
            user.user_image = None
            user.save()
            users.append(user)

        # ---------- FOLLOWS ----------
        for user in users:
            others = [u for u in users if u != user]
            for target in random.sample(others, k=2):
                Follow.objects.get_or_create(follower=user, following=target)

        # ---------- HASHTAGS ----------
        hashtag_names = ["django", "python", "drf", "backend", "api", "dev", "tech"]
        hashtags = [Hashtag.objects.get_or_create(hashtag_name=name)[0] for name in hashtag_names]

        # ---------- POSTS ----------
        posts = []
        for _ in range(6):
            author = random.choice(users)
            description = fake.paragraph(nb_sentences=3)
            post = Post.objects.create(
                author=author,
                description=description,
                music=None  # fake music placeholder
            )
            post.hashtags.set(random.sample(hashtags, k=2))
            post.people.set(random.sample(users, k=2))
            posts.append(post)

        # ---------- CONTENT ----------
        for post in posts:
            # fake content placeholder
            pass

        # ---------- POST LIKES ----------
        for post in posts:
            for user in random.sample(users, 3):
                PostLike.objects.get_or_create(user=user, post=post)

        # ---------- COMMENTS ----------
        comments = []
        for post in posts:
            for _ in range(2):
                comment = Comment.objects.create(
                    post=post,
                    user=random.choice(users),
                    text=fake.sentence(nb_words=8)
                )
                comments.append(comment)

        # ---------- COMMENT LIKES ----------
        for comment in comments:
            for user in random.sample(users, 2):
                CommentLike.objects.get_or_create(user=user, comment=comment)

        # ---------- SAVED POSTS ----------
        for user in users:
            save_post, _ = SavePost.objects.get_or_create(user=user)
            for post in random.sample(posts, k=2):
                SavePostItem.objects.get_or_create(save_post=save_post, post=post)

        # ---------- STORIES ----------
        for user in users:
            Stories.objects.create(
                user=user,
                file=None  # fake story placeholder
            )

        self.stdout.write(self.style.SUCCESS("✅ Realistic info seeded successfully!"))
