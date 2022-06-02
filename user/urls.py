from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
]
urlpatterns += router.urls
