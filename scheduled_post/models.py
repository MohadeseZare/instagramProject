from django.db import models


class ScheduledPost(models.Model):
    image = models.FileField(upload_to='posts/', null=True)
    caption = models.TextField(max_length=2200)
    tags = models.CharField(max_length=30, blank=True)
    creation_time = models.DateTimeField()
    active_comment = models.BooleanField(default=True)
    show_like_view = models.BooleanField(default=True)
