from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from instagram.client import InstagramAPI
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'followers_count', 'posts_count', 'following_count']

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        return attrs

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            access_token = Token.objects.create(user=instance)
            # api = InstagramAPI(access_token=access_token.key, client_secret='445zare0033841', client_id='m_zare.69')
            # recent_media, next_ = api.user_recent_media(user_id=instance.pk, count=10)
            # for media in recent_media:
            #     print(media.caption.text)
