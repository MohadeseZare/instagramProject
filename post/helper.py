from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from follow.models import Relationship
from user.models import UserSetting, UserLog
from .models import Post, Comment
from instagramProject.instagram_api_functions import (get_user_feed, get_feed_timeline, get_comments_media)


def get_all_post_current_user(current_user):
    results = get_user_feed()
    items = [item for item in results.get('items', [])]
    for post_item in items:
        if not Post.objects.filter(instagram_post_id=post_item['pk']).exclude():
            save_post(post_item)

    current_user.posts_count = items.__len__()
    current_user.save()


def get_timeline(current_instagram_user_id):
    results = get_feed_timeline()
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
    results = get_comments_media(post.instagram_post_id)
    items = [item for item in results.get('comments', [])]
    for item in items:
        comment = Comment.objects.filter(instagram_comment_id=item['pk'])
        if not comment:
            Comment.objects.create(instagram_comment_id=item['pk'],
                                   post=post, comment=item['text'], created_by=item['user']['pk'])


def validate_count_likes_per_hour(current_user):
    time_threshold = get_time_threshold()
    user_setting = UserSetting.objects.get(user=current_user)
    count_like_post = UserLog.objects.count(user=current_user, action=UserLog.Action.POST_LIKE,
                                            action_date__lte=time_threshold,
                                            action_date__gte=datetime.now())
    if user_setting.number_of_likes_per_hour < count_like_post:
        raise ValidationError("You did 300 likes in the last 24 hours.")
    else:
        return True


def validate_count_likes_per_day(current_user):
    today_min, today_max = get_range_date_today()
    user_setting = UserSetting.objects.get(user=current_user)
    count_like_post = UserLog.objects.count(user=current_user, action=UserLog.Action.POST_LIKE,
                                            action_date__range=(today_min, today_max))
    if user_setting.number_of_likes_per_day < count_like_post:
        raise ValidationError("You did 7000 likes today.")
    else:
        return True


def validate_count_comment_per_hour(current_user):
    time_threshold = get_time_threshold()
    user_setting = UserSetting.objects.get(user=current_user)
    count_like_post = UserLog.objects.count(user=current_user, action=UserLog.Action.COMMENT,
                                            action_date__lte=time_threshold,
                                            action_date__gte=datetime.now())
    if user_setting.number_of_comments_per_hour < count_like_post:
        raise ValidationError("You made 59 comments in the last 24 hours.")
    else:
        return True


def validate_count_comment_per_day(current_user):
    today_min, today_max = get_range_date_today()
    user_setting = UserSetting.objects.get(user=current_user)
    count_like_post = UserLog.objects.count(user=current_user, action=UserLog.Action.COMMENT,
                                            action_date__range=(today_min, today_max))
    if user_setting.number_of_comments_per_day < count_like_post:
        raise ValidationError("You made 500 comments today")
    else:
        return True


def get_range_date_today():
    today_min = datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.combine(datetime.date.today(), datetime.time.max)
    return today_min, today_max


def get_time_threshold():
    return datetime.now() - timedelta(hours=24)
