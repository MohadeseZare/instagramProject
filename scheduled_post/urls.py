from rest_framework.routers import DefaultRouter
from .views import ScheduledPostViewSet

router = DefaultRouter()
router.register(r'', ScheduledPostViewSet, basename='scheduled_post')
urlpatterns = router.urls
