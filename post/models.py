from django.db import models
import jsonfield
from user.models import User


class Post(models.Model):
    class PostType(models.TextChoices):
        PHOTO = '1'
        VIDEO = '2'
        CAROUSEL = '8'

    instagram_post_id = models.IntegerField(null=True, blank=True)
    instagram_post_media_path = jsonfield.JSONField(default=list)
    media_file = models.FileField(upload_to='posts/', null=True, blank=True)
    caption = models.TextField(max_length=2200)
    tags = models.CharField(max_length=30,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
    active_comment = models.BooleanField(default=True)
    show_like_view = models.BooleanField(default=True)
    media_type = models.CharField(blank=True, null=True, choices=PostType.choices, max_length=1)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    instagram_comment_id = models.IntegerField(null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()
