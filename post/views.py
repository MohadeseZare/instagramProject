from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, TimeLineSerializer
from .permissions import IsOwnerOrReadOnly
from user.models import User
from follow.models import Relationship
from instagramProject.instagram_api_functions import (get_user_feed, get_feed_timeline, get_comments_media,
                                                      media_like, media_unlike, delete_comment_media,
                                                      comment_like, comment_unlike)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        results = get_user_feed()
        items = [item for item in results.get('items', [])]
        for post_item in items:
            if not Post.objects.filter(instagram_post_id=post_item['pk']).exclude():
                Post.objects.create(instagram_post_id=post_item['pk'], created_by=self.request.user,
                                    caption=post_item['caption']['text'],
                                    media_file=post_item['image_versions2']['candidates'][0]['url'])

        self.request.user.posts_count = items.__len__()
        self.request.user.save()
        return Post.objects.filter(created_by=self.request.user)


class TimelineViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TimeLineSerializer

    def get_queryset(self):
        results = get_feed_timeline()
        items = [item for item in results.get('feed_items', [])
                 if item.get('media_or_ad')]
        for item in items:
            if not Post.objects.filter(instagram_post_id=item['media_or_ad']['pk']).exclude():
                user = User.objects.get(instagram_user_id=item['media_or_ad']['user']['pk'])
                if not user:
                    user = User.objects.create_user(username=item['media_or_ad']['user']['username'],
                                                    instagram_user_id=item['media_or_ad']['user']['pk'])
                    Relationship.objects.update_or_create(current_user=self.request.user,
                                                          target_user=user)

                Post.objects.create(instagram_post_id=item['media_or_ad']['pk'], created_by=user,
                                    caption=item['media_or_ad']['caption']['text'],
                                    media_file=" ")
        return Post.objects.filter(Q(created_by__target_user__current_user=self.request.user) |
                                   Q(created_by=self.request.user))

    def like_post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        media_like(post.instagram_post_id)
        queryset = Post.objects.filter(Q(created_by__target_user__current_user=self.request.user) |
                                       Q(created_by=self.request.user))
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def unlike_post(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        media_unlike(post.instagram_post_id)
        queryset = Post.objects.filter(Q(created_by__target_user__current_user=self.request.user) |
                                       Q(created_by=self.request.user))
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        results = get_comments_media(post.instagram_post_id)
        items = [item for item in results.get('comments', [])]
        for item in items:

            user = User.objects.get(instagram_user_id=item['user']['pk'])
            if not user:
                user = User.objects.create_user(username=item['user']['username'],
                                                instagram_user_id=item['user']['pk'])
            comment = Comment.objects.filter(instagram_comment_id=item['pk'])
            if not comment:
                Comment.objects.create(instagram_comment_id=item['pk'],
                                       post=post, comment=item['text'], created_by=user)

        queryset = Comment.objects.filter(post_id=post.id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        state = delete_comment_media(comment.post.instagram_post_id, comment.instagram_comment_id)
        if state['status'] == 'ok':
            comment.delete()
        queryset = Comment.objects.filter(post_id=comment.post.id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def like_comment(self, request, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        comment_like(comment.instagram_comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def unlike_comment(self, request, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        comment_unlike(comment.instagram_comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
