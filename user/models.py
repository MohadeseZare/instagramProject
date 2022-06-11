from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    instagram_password = models.CharField(null=True, max_length=200)
    instagram_user_id = models.IntegerField(null=True)
