from django.db.models import Q
from follow.models import Relationship
from .models import Post, Comment
from instagramProject.instagram_api_functions import InstagramAPI

api = InstagramAPI()


def get_all_post_current_user(current_user):
    results = api.get_user_feed()
    items = [item for item in results.get('items', [])]
    for post_item in items:
        if not Post.objects.filter(instagram_post_id=post_item['pk']).exclude():
            save_post(post_item)

    current_user.posts_count = items.__len__()
    current_user.save()


def get_timeline(current_instagram_user_id):
    results = api.get_feed_timeline()
    items = [item for item in results.get('feed_items', [])
             if item.get('media_or_ad')]
    for item in items:
        if not Post.objects.filter(instagram_post_id=item['media_or_ad']['pk']).exclude():
            save_post(item['media_or_ad'])
        if not Relationship.objects.filter(Q(current_instagram_user_id=current_instagram_user_id) |
                                           Q(current_instagram_user_id=item['media_or_ad']['user']['pk'])):
            Relationship.objects.create(current_instagram_user_id=current_instagram_user_id,
                                        target_instagram_user_id=item['media_or_ad']['user']['pk'],
                                        instagram_username=item['media_or_ad']['user']['username'])


def save_post(post_item):
    Post.objects.create(instagram_post_id=post_item['pk'], created_by=post_item['caption']['user_id'],
                        caption=post_item['caption']['text'],
                        instagram_post_media_path=post_item['image_versions2']['candidates'])


def get_list_comment_by_post_id(post_id):
    post = Post.objects.get(id=post_id)
    results = api.get_comments_media(post.instagram_post_id)
    items = [item for item in results.get('comments', [])]
    for item in items:
        comment = Comment.objects.filter(instagram_comment_id=item['pk'])
        if not comment:
            Comment.objects.create(instagram_comment_id=item['pk'],
                                   post=post, comment=item['text'], created_by=item['user']['pk'])




