# import datetime
# import celery
# from celery import shared_task
# from django.utils import timezone
# from .models import ScheduledPost
# from post.serializers import PostSerializer
# from post.models import Post
#
#
# @celery.decorators.periodic_task(
#     run_every=datetime.timedelta(minutes=1))  # here we assume we want it to be run every 1 mins
# # @shared_task
# def scheduled_task():
#     list_post = ScheduledPost.objects.get(creation_at=timezone.now())
#     items = [item for item in list_post]
#     for item in items:
#         post = Post()
#         post.caption = item['caption']
#         post.media_file = item['media_file']
#         serializer = PostSerializer(data=post)
#         if serializer.is_valid():
#             serializer.save()
#     return 0
