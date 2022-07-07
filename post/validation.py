from django.core.exceptions import ValidationError
from datetime import datetime
from user.models import UserSetting, UserLog
from instagramProject.datetime_helper import DatetimeHelper


class PostValidation:
    @staticmethod
    def validate_count_likes_per_hour(current_user):
        time_threshold = DatetimeHelper.get_time_threshold()
        user_setting = UserSetting.objects.get(user=current_user)
        count_like_post = UserLog.objects.filter(user=current_user, action=UserLog.Action.POST_LIKE,
                                                 action_date__lte=time_threshold,
                                                 action_date__gte=datetime.now()).count()
        if user_setting.number_of_likes_per_hour < count_like_post:
            raise ValidationError("You did 300 likes in the last 24 hours.")
        else:
            return True

    @staticmethod
    def validate_count_likes_per_day(current_user):
        today_min, today_max = DatetimeHelper.get_range_date_today()
        user_setting = UserSetting.objects.get(user=current_user)
        count_like_post = UserLog.objects.filter(user=current_user, action=UserLog.Action.POST_LIKE,
                                                 action_date__range=(today_min, today_max)).count()
        if user_setting.number_of_likes_per_day < count_like_post:
            raise ValidationError("You did 7000 likes today.")

    @staticmethod
    def validate_count_comment_per_hour(current_user):
        time_threshold = DatetimeHelper.get_time_threshold()
        user_setting = UserSetting.objects.get(user=current_user)
        count_like_post = UserLog.objects.filter(user=current_user, action=UserLog.Action.COMMENT,
                                                 action_date__lte=time_threshold,
                                                 action_date__gte=datetime.now()).count()
        if user_setting.number_of_comments_per_hour < count_like_post:
            raise ValidationError("You made 59 comments in the last 24 hours.")

    @staticmethod
    def validate_count_comment_per_day(current_user):
        today_min, today_max = DatetimeHelper.get_range_date_today()
        user_setting = UserSetting.objects.get(user=current_user)
        count_like_post = UserLog.objects.filter(user=current_user, action=UserLog.Action.COMMENT,
                                                 action_date__range=(today_min, today_max)).count()
        if user_setting.number_of_comments_per_day < count_like_post:
            raise ValidationError("You made 500 comments today")
