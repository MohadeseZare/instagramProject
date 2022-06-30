# Generated by Django 3.2.13 on 2022-06-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_remove_post_file_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media_type',
            field=models.CharField(blank=True, choices=[('1', 'Photo'), ('2', 'Video'), ('8', 'Carousel')], max_length=1, null=True),
        ),
    ]
