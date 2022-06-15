from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ["id", "image", "caption", 'tags', "created_by", 'active_comment', 'show_like_view']


class TimeLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "image", "caption", 'tags', "created_by"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("id", "comment", "user")
