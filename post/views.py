from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, TimeLineSerializer
from .permissions import IsOwnerOrReadOnly
from user.models import User
from follow.models import Relationship
from instagramProject.instagram_api_functions import get_user_feed, get_feed_timeline


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
                                    image=post_item['image_versions2']['candidates'][0]['url'])

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
                user = User.objects.filter(instagram_user_id=item['media_or_ad']['user']['pk'])
                if not user:
                    user = User.objects.create_user(username=item['media_or_ad']['user']['username'],
                                                    instagram_user_id=item['media_or_ad']['user']['pk'])
                    Relationship.objects.update_or_create(current_user=self.request.user,
                                                          target_user=user)
                else:
                    user = user.first()

                Post.objects.create(instagram_post_id=item['media_or_ad']['pk'], created_by=user,
                                    caption=item['media_or_ad']['caption']['text'],
                                    image=" ")
        return Post.objects.filter(Q(created_by__target_user__current_user=self.request.user) |
                                   Q(created_by=self.request.user))


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
