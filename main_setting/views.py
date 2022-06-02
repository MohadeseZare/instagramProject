from rest_framework import viewsets, permissions
from .models import MainSetting
from .serializers import MainSettingSerializer


class MainSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = MainSetting.objects.all()
    serializer_class = MainSettingSerializer
