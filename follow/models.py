from django.db import models


class Relationship(models.Model):
    current_instagram_user_id = models.IntegerField()
    target_instagram_user_id = models.IntegerField()
    instagram_username = models.CharField(max_length=200)



