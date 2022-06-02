from rest_framework.routers import DefaultRouter
from .views import UserSettingViewSet

router = DefaultRouter()
router.register(r'', UserSettingViewSet, basename='user_setting')
urlpatterns = router.urls
