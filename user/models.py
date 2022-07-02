from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    instagram_password = models.CharField(null=True, max_length=200)
    instagram_user_id = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        UserSetting.objects.get_or_create(user=self)


class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_followers_per_hour = models.IntegerField(default=10)
    number_of_followers_per_day = models.IntegerField(default=200)
    number_of_unfollowers_per_day = models.IntegerField(default=70)
    number_of_likes_per_hour = models.IntegerField(default=300)
    number_of_likes_per_day = models.IntegerField(default=7000)
    number_of_comments_per_hour = models.IntegerField(default=59)
    number_of_comments_per_day = models.IntegerField(default=500)
    number_of_hashtags_used_in_the_post = models.IntegerField(default=30)
    number_of_caption_words = models.IntegerField(default=2200)
    number_of_comment_words = models.IntegerField(default=240)


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
