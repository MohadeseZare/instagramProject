from django.conf import settings
from django.contrib.auth.hashers import make_password
from instagram_private_api import Client, ClientLoginError
from rest_framework import serializers
from .models import User, UserLog, UserSetting
from instagramProject.instagram_api_functions import InstagramAPI


class UserSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        try:
            settings.CURRENT_USER_INSTAGRAM_USERNAME = attrs["username"]
            settings.CURRENT_USER_INSTAGRAM_PASSWORD = attrs["password"]
            api = InstagramAPI()
            user_id = api.get_authenticated_user_id()
            user_instagram = api.user_info(user_id)
            attrs["followers_count"] = user_instagram['user']['follower_count']
            attrs["following_count"] = user_instagram['user']['following_count']
            attrs["posts_count"] = user_instagram['user']['media_count']
            attrs["instagram_user_id"] = user_id
            attrs["instagram_password"] = attrs["password"]
            attrs["password"] = make_password(attrs["password"])
        except ClientLoginError:
            raise ValueError("Wrong username or password.")
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'followers_count', 'posts_count', 'following_count']


class UserSettingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSetting
        fields = '__all__'


class UserLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserLog
        fields = '__all__'
