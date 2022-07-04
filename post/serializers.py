from rest_framework import serializers

from user.models import UserLog
from .models import Post, Comment
from .validation import PostValidation
from instagramProject.instagram_api_functions import InstagramAPI


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
        if PostValidation.validate_count_comment_per_day(self.context['request'].user) & \
                PostValidation.validate_count_comment_per_hour(self.context['request'].user):
            post = Post.objects.get(id=self.context['view'].kwargs['post_id'])
            api = InstagramAPI()
            comment_insta = api.post_comment_media(post.instagram_post_id, attrs['comment'])
            UserLog.objects.create(action=UserLog.Action.COMMENT, user=self.context['request'].user)
            attrs['post'] = post
            attrs['instagram_comment_id'] = comment_insta['comment']['pk']
            attrs['created_by'] = self.context['request'].user.instagram_user_id
        return attrs

    class Meta:
        model = Comment
        fields = ("id", "comment", "created_by")
