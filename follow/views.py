from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import RelationshipSerializer
from .models import Relationship
from .validation import ValidateFollower
from user.models import UserLog
from instagramProject.instagram_api_functions import InstagramAPI

api = InstagramAPI()


class FollowingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer

    def list(self, request):
        results = api.get_user_following()
        items = [item for item in results.get('users', [])]
        for item in items:
            Relationship.objects.update_or_create(current_instagram_user_id=self.request.user.instagram_user_id,
                                                  target_instagram_user_id=item['pk'],
                                                  instagram_username=item['username'])
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        if ValidateFollower.validate_count_follows_per_hour(self.request.user) \
                | ValidateFollower.validate_count_follows_per_day(self.request.user):
            user_id = api.get_username_info(kwargs['username'])
            following_state = api.follow_user(user_id)
            if following_state['friendship_status']['following']:
                Relationship.objects.update_or_create(current_instagram_user_id=self.request.user.instagram_user_id,
                                                      target_instagram_user_id=user_id,
                                                      instagram_username=kwargs['username'])
                UserLog.objects.create(user=self.request.user, action=UserLog.Action.FOLLOW)
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, **kwargs):
        if ValidateFollower.validate_count_unfollow(self.request.user):
            user_id = api.get_username_info(kwargs['username'])
            api.unfollow_user(user_id)

            Relationship.objects.get(current_instagram_user_id=self.request.user.instagram_user_id,
                                     target_instagram_user_id=user_id).delete()
            UserLog.objects.create(user=self.request.user, action=UserLog.Action.UNFOLLOW)
        queryset = Relationship.objects.filter(current_instagram_user_id=self.request.user.instagram_user_id)
        serializer = RelationshipSerializer(queryset, many=True)
        return Response(serializer.data)


class FollowersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer

    def get_queryset(self, *args, **kwargs):
        results = api.get_user_follows()
        items = [item for item in results.get('users', [])]
        for item in items:
            Relationship.objects.update_or_create(current_instagram_user_id=item['pk'],
                                                  instagram_username=item['username'],
                                                  target_instagram_user_id=self.request.user.instagram_user_id)
        return Relationship.objects.filter(target_instagram_user_id=self.request.user.instagram_user_id)
