from django.core.files import File
import requests
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

from user.models import User
from follow.models import Relationship
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from instagramProject.instagram_api_functions import (get_user_feed, get_feed_timeline, get_comments_media,
                                                      media_like, media_unlike, delete_comment_media,
                                                      comment_like, comment_unlike)


def get_all_post_current_user(current_user):
    results = get_user_feed()
    items = [item for item in results.get('items', [])]
    for post_item in items:
        if not Post.objects.filter(instagram_post_id=post_item['pk']).exclude():
            save_post(post_item)

    current_user.posts_count = items.__len__()
    current_user.save()


def get_timeline(current_user):
    results = get_feed_timeline()
    items = [item for item in results.get('feed_items', [])
             if item.get('media_or_ad')]
    for item in items:
        if not Post.objects.filter(instagram_post_id=item['media_or_ad']['pk']).exclude():
            user = User.objects.get(instagram_user_id=item['media_or_ad']['user']['pk'])
            if not user:
                user = User.objects.create_user(username=item['media_or_ad']['user']['username'],
                                                instagram_user_id=item['media_or_ad']['user']['pk'])
                Relationship.objects.update_or_create(current_user=current_user,
                                                      target_user=user)
            save_post(item['media_or_ad'])


def save_post(post_item):
    user = User.objects.get(instagram_user_id=post_item['caption']['user_id'])
    path_media = ""
    if post_item['media_type'] != 8:
        path_media = post_item['image_versions2']['candidates'][0]['url']
    Post.objects.create(instagram_post_id=post_item['pk'], created_by=user,
                        caption=post_item['caption']['text'],
                        instagram_post_media_path=path_media)


def get_list_comment_by_post_id(post_id):
    post = Post.objects.get(id=post_id)
    results = get_comments_media(post.instagram_post_id)
    items = [item for item in results.get('comments', [])]
    for item in items:
        user = User.objects.get(instagram_user_id=item['user']['pk'])
        if not user:
            user = User.objects.create_user(username=item['user']['username'],
                                            instagram_user_id=item['user']['pk'])
        comment = Comment.objects.filter(instagram_comment_id=item['pk'])
        if not comment:
            Comment.objects.create(instagram_comment_id=item['pk'],
                                   post=post, comment=item['text'], created_by=user)
