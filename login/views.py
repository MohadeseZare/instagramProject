from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
# from rest_auth.serializers import LoginSerializer
from rest_auth.views import LoginView
from user.models import User
from rest_framework import generics
UserModel = get_user_model()


class LoginViewSet(LoginView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = LoginSerializer
