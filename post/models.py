from django.db import models
from user.models import User


class Post(models.Model):
    instagram_post_id = models.IntegerField(null=True)
    image = models.FileField(upload_to='posts/', null=True)
    caption = models.TextField(max_length=2200)
    tags = models.CharField(max_length=30,  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="user", on_delete=models.DO_NOTHING)
    active_comment = models.BooleanField(default=True)
    show_like_view = models.BooleanField(default=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    instagram_comment_id = models.IntegerField(null=True)
    comment = models.TextField()
    created_by = models.DateTimeField(auto_now_add=True)
    created_at = models.ForeignKey(User, on_delete=models.DO_NOTHING)
