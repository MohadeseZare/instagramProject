from rest_framework import viewsets, permissions, generics
from rest_framework.utils import json

from .serializers import UserSerializer, UserSettingSerializer
from .models import User, UserSetting
from .helper import UserSettingHelper


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class UserSettingViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSettingSerializer

    def get_object(self):
        user_setting = UserSetting.objects.get(user=self.request.user)
        return user_setting

    def get_queryset(self):
        user_setting = UserSetting.objects.get(user=self.request.user)
        return user_setting

    def put(self, request, *args, **kwargs):
        UserSettingHelper.checked_for_update_setting(request)
        return self.update(request, *args, **kwargs)
