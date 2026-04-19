from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=100)
    profile_pic = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    post_id = models.CharField(max_length=36, primary_key=True)
    content = models.CharField(max_length=1000)
    posted_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"Post by {self.posted_by.name} at {self.posted_at}"


class Comment(models.Model):
    commented_id = models.CharField(max_length=36, primary_key=True)
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(default=timezone.now)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Comment by {self.commented_by.name} at {self.commented_at}"


class Reaction(models.Model):
    WOW = "WOW"
    LIT = "LIT"
    LOVE = "LOVE"
    HAHA = "HAHA"
    THUMBS_UP = "THUMBS-UP"
    THUMBS_DOWN = "THUMBS-DOWN"
    ANGRY = "ANGRY"
    SAD = "SAD"

    REACTION_CHOICES = [
        (WOW, WOW),
        (LIT, LIT),
        (LOVE, LOVE),
        (HAHA, HAHA),
        (THUMBS_UP, THUMBS_UP),
        (THUMBS_DOWN, THUMBS_DOWN),
        (ANGRY, ANGRY),
        (SAD, SAD),
    ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions",
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="reactions",
        null=True,
        blank=True,
    )
    reaction = models.CharField(max_length=100, choices=REACTION_CHOICES)
    reacted_at = models.DateTimeField(default=timezone.now)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")