from rest_framework import serializers
from .models import Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['current_instagram_user_id', 'target_instagram_user_id', 'instagram_username']
