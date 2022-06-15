from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TimelineViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')

urlpatterns = [
     # path("", PostViewSet.as_view({'get': 'list'}), name="post"),
     path("timeline/", TimelineViewSet.as_view({'get': 'list'}), name="timeline"),
    # path("search", TimelineList.as_view(), name="search"),
    # path("<int:pk>/", UpdatePost, name="update_post")
    # path('<int:post_id>/comment/', CommentViewSet),
    # path('<int:post_id>/comment/<int:comment_id>', CommentViewSet),
]
urlpatterns += router.urls
