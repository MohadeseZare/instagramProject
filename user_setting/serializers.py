from rest_framework import serializers
from .models import UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSetting
        fields = '__all__'
