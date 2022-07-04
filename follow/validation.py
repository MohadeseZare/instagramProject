from datetime import datetime
from django.core.exceptions import ValidationError
from instagramProject.datetime_helper import DatetimeHelper
from user.models import UserLog, UserSetting


class ValidateFollower:
    @staticmethod
    def validate_count_follows_per_hour(current_user):
        time_threshold = DatetimeHelper.get_time_threshold()
        user_setting = UserSetting.objects.get(user=current_user)
        count_follow_user = UserLog.objects.filter(user=current_user, action=UserLog.Action.FOLLOW,
                                                   action_date__lte=time_threshold,
                                                   action_date__gte=datetime.now()).count()
        if user_setting.number_of_followers_per_hour < count_follow_user:
            raise ValidationError("You had 10 followers in the last 24 hours and you can't follow anymore.")
        else:
            return True

    @staticmethod
    def validate_count_follows_per_day(current_user):
        today_min, today_max = DatetimeHelper.get_range_date_today()
        user_setting = UserSetting.objects.get(user=current_user)
        count_follow_user = UserLog.objects.filter(user=current_user, action=UserLog.Action.FOLLOW,
                                                   action_date__range=(today_min, today_max)).count()
        if user_setting.number_of_followers_per_hour < count_follow_user:
            raise ValidationError("You have followed 200 times today, you can no longer follow.")
        else:
            return True

    @staticmethod
    def validate_count_unfollow(self, current_user):
        today_min, today_max = DatetimeHelper.get_range_date_today()
        user_setting = UserSetting.objects.get(user=current_user)
        count_unfollow_user = UserLog.objects.filter(user=current_user, action=UserLog.Action.UNFOLLOW,
                                                     action_date__range=(today_min, today_max)).count()
        if user_setting.number_of_unfollowers_per_day < count_unfollow_user:
            raise ValidationError("You have done 70 unfollows today, you can no longer follow.")
        else:
            return True
