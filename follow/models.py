from django.db import models
from django.contrib.auth import get_user_model


class Relationship(models.Model):
    current_user = models.ForeignKey(get_user_model(), related_name="current_user", on_delete=models.DO_NOTHING)
    target_user = models.ForeignKey(get_user_model(), null=True,
                                    related_name="target_user", on_delete=models.DO_NOTHING)
