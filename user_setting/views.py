from rest_framework import viewsets, permissions
from .models import UserSetting
from .serializers import UserSettingSerializer


class UserSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
