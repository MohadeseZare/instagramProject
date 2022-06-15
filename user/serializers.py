from django.contrib.auth.hashers import make_password
from instagram_private_api import Client, ClientLoginError
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        try:
            api = Client(attrs["username"], attrs["password"], auto_patch=True)
            user_id = api.authenticated_user_id
            user_instagram = api.user_info(user_id)
            attrs["followers_count"] = user_instagram['user']['follower_count']
            attrs["following_count"] = user_instagram['user']['following_count']
            attrs["posts_count"] = user_instagram['user']['media_count']
            attrs["instagram_user_id"] = user_id
            attrs["instagram_password"] = attrs["password"]
            attrs["password"] = make_password(attrs["password"])
        except ClientLoginError:
            raise ValueError("Wrong username or password")
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'followers_count', 'posts_count', 'following_count']

