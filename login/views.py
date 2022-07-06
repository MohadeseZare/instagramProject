from django.contrib.auth import get_user_model, login
from rest_framework import permissions

from .serializers import LoginSerializer
from rest_auth.views import LoginView as RestLoginView
UserModel = get_user_model()


class LoginViewSet(RestLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

