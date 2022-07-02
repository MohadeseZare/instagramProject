from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, UserSettingSerializer
from .models import User, UserSetting


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


class UserSettingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSettingSerializer

    def update(self, request, pk=None):
        user_setting = UserSetting.objects.update_or_create(request.data, user=self.request.user)
        serializer = UserSettingSerializer(user_setting)
        return Response(serializer.data)
