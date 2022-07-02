from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import RelationshipSerializer
from .models import Relationship
from user.models import UserLog
from user.serializers import UserLogSerializer
from instagramProject.instagram_api_functions import (get_user_following, get_user_follows,
                                                      follow_user, get_username_info,
                                                      unfollow_user)


class FollowingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer

    def list(self, request):
        results = get_user_following()
        items = [item for item in results.get('users', [])]
        for item in items:
            Relationship.objects.update_or_create(current_instagram_user_id=self.request.user.instagram_user_id,
                                                  target_instagram_user_id=item['pk'],
                                                  instagram_username=item['username'])
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        user_id = get_username_info(kwargs['username'])
        following_state = follow_user(user_id)
        if following_state['friendship_status']['following']:
            Relationship.objects.update_or_create(current_instagram_user_id=self.request.user.instagram_user_id,
                                                  target_instagram_user_id=user_id,
                                                  instagram_username=kwargs['username'])
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        user_id = get_username_info(kwargs['username'])
        unfollow_user(user_id)

        Relationship.objects.get(current_instagram_user_id=self.request.user.instagram_user_id,
                                 target_instagram_user_id=user_id).delete()
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)


class FollowersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer

    def get_queryset(self, *args, **kwargs):
        results = get_user_follows()
        items = [item for item in results.get('users', [])]
        for item in items:
            Relationship.objects.update_or_create(current_instagram_user_id=item['pk'],
                                                  instagram_username=item['username'],
                                                  target_instagram_user_id=self.request.user.instagram_user_id)
        return Relationship.objects.filter(target_instagram_user_id=self.request.user.instagram_user_id)
