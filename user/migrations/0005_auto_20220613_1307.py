# Generated by Django 3.2.13 on 2022-06-13 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_relationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationship',
            name='target',
        ),
        migrations.AddField(
            model_name='relationship',
            name='target_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='target_user', to=settings.AUTH_USER_MODEL),
        ),
    ]