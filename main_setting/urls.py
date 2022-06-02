from rest_framework.routers import DefaultRouter
from .views import MainSettingViewSet

router = DefaultRouter()
router.register(r'', MainSettingViewSet, basename='main_setting')
urlpatterns = router.urls
