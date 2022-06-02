from rest_framework import serializers
from .models import ScheduledPost


class ScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPost
        fields = '__all__'
