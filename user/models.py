from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    instagram_password = models.CharField(null=True, max_length=200)
    instagram_user_id = models.IntegerField(null=True)


class UserLog(models.Model):
    class Action(models.TextChoices):
        POST = 'post'
        POST_LIKE = 'post_like'
        POST_UNLIKE = 'post_unlike'
        COMMENT = 'comment'
        COMMENT_DELETE = 'comment_delete'
        COMMENT_LIKE = 'comment_like'
        COMMENT_UNLIKE = 'comment_unlike'
        FOLLOW = 'follow'
        UNFOLLOW = 'unfollow'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    action = models.CharField(blank=True, choices=Action.choices, max_length=14)
    action_date = models.DateTimeField(auto_now_add=True)
