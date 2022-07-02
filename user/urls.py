from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSettingViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = [
    path("setting/", UserSettingViewSet.as_view({'patch': 'update'}), name="user_setting"),
    ]
urlpatterns += router.urls

