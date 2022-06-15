# from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import LoginViewSet

# router = DefaultRouter()
# router.register(r'', LoginViewSet, basename='login')

urlpatterns = [
    path(r'', LoginViewSet.as_view(), name="login"),
]
