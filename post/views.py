from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.response import Response

from user.models import UserLog
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, TimeLineSerializer
from .permissions import IsOwnerOrReadOnly
from .helper import get_all_post_current_user, get_timeline, get_list_comment_by_post_id
from follow.models import Relationship
from instagramProject.instagram_api_functions import (get_comments_media,
                                                      media_like, media_unlike, delete_comment_media,
                                                      comment_like, comment_unlike)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user.instagram_user_id)

    def list(self, request, **kwargs):
        get_all_post_current_user(self.request.user)
        queryset = Post.objects.filter(created_by=self.request.user.instagram_user_id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class TimelineViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TimeLineSerializer

    def get_queryset(self):
        get_timeline(self.request.user.instagram_user_id)
        follower_query = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)\
            .values_list('target_instagram_user_id', flat=True)
        return Post.objects.filter(Q(created_by__in=follower_query) |
                                   Q(created_by=self.request.user.instagram_user_id))

    def like_post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        media_like(post.instagram_post_id)
        UserLog.objects.create(action=UserLog.Action.POST_LIKE)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def unlike_post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        media_unlike(post.instagram_post_id)
        UserLog.objects.create(action=UserLog.Action.POST_UNLIKE)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, **kwargs):
        get_list_comment_by_post_id(kwargs['post_id'])
        queryset = Comment.objects.filter(post_id=kwargs['post_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        state = delete_comment_media(comment.post.instagram_post_id, comment.instagram_comment_id)
        if state['status'] == 'ok':
            comment.delete()
        queryset = Comment.objects.filter(post_id=comment.post.id)
        UserLog.objects.create(action=UserLog.Action.COMMENT_DELETE)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def like_comment(self, request, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        comment_like(comment.instagram_comment_id)
        UserLog.objects.create(action=UserLog.Action.COMMENT_LIKE)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def unlike_comment(self, request, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        comment_unlike(comment.instagram_comment_id)
        UserLog.objects.create(action=UserLog.Action.COMMENT_UNLIKE)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
