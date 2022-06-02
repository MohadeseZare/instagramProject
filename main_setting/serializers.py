from rest_framework import serializers
from .models import MainSetting


class MainSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainSetting
        fields = '__all__'
