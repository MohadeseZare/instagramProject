from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "image", "caption", "created_by"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "comment", "user")
