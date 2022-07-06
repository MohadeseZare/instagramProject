from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MainSettingViewSet

router = DefaultRouter()
urlpatterns = [
    path(r"", MainSettingViewSet.as_view(), name="main_setting"),
]
urlpatterns += router.urls
