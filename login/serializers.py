from django.contrib.auth import authenticate
from rest_framework import serializers
from django.conf import settings
from user.models import User
from instagramProject.instagram_api_functions import InstagramAPI


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=('Username'), max_length=254,
    )

    password = serializers.CharField(
        label=('Password'), write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)
                if user:
                    if user.instagram_user_id:
                        InstagramAPI(username, password)

            else:
                msg = 'username is not registered.'
                raise serializers.ValidationError(msg)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs

