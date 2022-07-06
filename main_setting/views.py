from rest_framework import viewsets, permissions, generics
from .models import MainSetting
from .serializers import MainSettingSerializer


class MainSettingViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = MainSettingSerializer

    def get_object(self):
        main_setting = MainSetting.objects.first()
        return main_setting

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
