from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls
