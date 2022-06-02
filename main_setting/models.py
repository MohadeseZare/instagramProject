from django.db import models


class MainSetting(models.Model):
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
