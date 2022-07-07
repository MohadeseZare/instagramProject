from rest_framework.exceptions import ValidationError
from main_setting.models import MainSetting


class UserSettingHelper:

    @staticmethod
    def checked_for_update_setting(request):
        data = request.data
        main_setting = MainSetting.objects.first()
        if (main_setting.number_of_followers_per_hour <
                int(data['number_of_followers_per_hour'])):
            raise ValidationError("number of followers per hour more is main setting.")
        if (main_setting.number_of_followers_per_day <
                int(data['number_of_followers_per_day'])):
            raise ValidationError("number of followers per day more is main setting.")
        if (main_setting.number_of_unfollowers_per_day <
                int(data['number_of_unfollowers_per_day'])):
            raise ValidationError("number of unfollowers per day more is main setting.")
        if (main_setting.number_of_likes_per_hour <
                int(data['number_of_likes_per_hour'])):
            raise ValidationError("number of likes per hour more is main setting.")
        if (main_setting.number_of_likes_per_day <
                int(data['number_of_likes_per_day'])):
            raise ValidationError("number of likes per day more is main setting.")
        if (main_setting.number_of_comments_per_hour <
                int(data['number_of_comments_per_hour'])):
            raise ValidationError("number of comments per hour more is main setting.")
        if (main_setting.number_of_comments_per_day <
                int(data['number_of_comments_per_day'])):
            raise ValidationError("number of comments per day more is main setting.")
        if (main_setting.number_of_hashtags_used_in_the_post <
                int(data['number_of_hashtags_used_in_the_post'])):
            raise ValidationError("number of hashtags used in the post more is main setting.")
        if (main_setting.number_of_caption_words <
                int(data['number_of_caption_words'])):
            raise ValidationError("number of caption words more is main setting.")
        if (main_setting.number_of_comment_words <
                int(data['number_of_comment_words'])):
            raise ValidationError("number of comment words more is main setting.")
