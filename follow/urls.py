from django.urls import path
from .views import FollowingViewSet, FollowersViewSet

urlpatterns = [
     path("following/", FollowingViewSet.as_view({'get': 'list'}), name="following"),
     path("followers/", FollowersViewSet.as_view({'get': 'list'}), name="followers"),
     path("<str:username>/follow/", FollowingViewSet.as_view({'get': 'create'}), name="follow"),
     path("<str:username>/unfollow/", FollowingViewSet.as_view({'get': 'destroy'}), name="un_follow"),
]