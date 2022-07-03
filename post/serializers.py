from rest_framework import serializers

from user.models import UserLog
from .models import Post, Comment
from instagramProject.instagram_api_functions import post_comment_media


class PostSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ["id", 'instagram_post_id', "media_file", "media_type", "caption", "tags", "created_by",
                  "active_comment", "show_like_view", 'instagram_post_media_path']


class TimeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", 'instagram_post_id', "media_file", "media_type", "caption", "tags", "created_by",
                  'instagram_post_media_path']


class CommentSerializer(serializers.ModelSerializer):
    def validate(self, attrs, **kwargs):
        post = Post.objects.get(id=self.context['view'].kwargs['post_id'])
        comment_insta = post_comment_media(post.instagram_post_id, attrs['comment'])
        UserLog.objects.create(action=UserLog.Action.COMMENT)
        attrs['post'] = post
        attrs['instagram_comment_id'] = comment_insta['comment']['pk']
        attrs['created_by'] = comment_insta['comment']['user']['pk']
        return attrs

    class Meta:
        model = Comment
        fields = ("id", "comment", "created_by")
