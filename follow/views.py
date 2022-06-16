from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import RelationshipSerializer
from .models import Relationship
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
            user = get_user_model().objects.filter(instagram_user_id=item['pk'])
            if not user:
                user = get_user_model().objects.create_user(username=item['username'],
                                                            instagram_user_id=item['pk'])
                Relationship.objects.update_or_create(current_user=self.request.user,
                                                      target_user=user)
        queryset = Relationship.objects.filter(current_user=self.request.user)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        user_id = get_username_info(kwargs['username'])
        following_state = follow_user(user_id)
        if following_state['friendship_status']['following']:
            user = get_user_model().objects.filter(instagram_user_id=user_id)
            if not user:
                user = get_user_model().objects.create_user(username=kwargs['username'],
                                                            instagram_user_id=user_id)
                Relationship.objects.update_or_create(current_user=self.request.user,
                                                      target_user=user)
        queryset = Relationship.objects.filter(current_user=self.request.user)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        user_id = get_username_info(kwargs['username'])
        unfollow_user(user_id)
        user = get_user_model().objects.get(instagram_user_id=user_id)
        if user:
            relationship = Relationship.objects.filter(current_user=self.request.user,
                                                       target_user__in=user).delete()
        queryset = Relationship.objects.filter(current_user=self.request.user)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)


class FollowersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer

    def get_queryset(self, *args, **kwargs):
        results = get_user_follows()
        items = [item for item in results.get('users', [])]
        for item in items:
            user = get_user_model().objects.filter(instagram_user_id=item['pk'])
            if not user:
                user = get_user_model().objects.create_user(username=item['username'],
                                                            instagram_user_id=item['pk'])
                Relationship.objects.update_or_create(current_user=user,
                                                      target_user=self.request.user)
        return Relationship.objects.filter(target_user=self.request.user)
