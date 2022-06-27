from django.urls import path

from .views import PostViewSet, CommentViewSet, TimelineViewSet

urlpatterns = [
     # post event
     path("", PostViewSet.as_view({'get': 'list'}), name="post"),
     path("add/", PostViewSet.as_view({'post': 'create'}), name="new_post"),

     # timeline event
     path("timeline/", TimelineViewSet.as_view({'get': 'list'}), name="timeline"),
     path('like/<int:post_id>/', TimelineViewSet.as_view({'get': 'like_post'})),
     path('unlike/<int:post_id>/', TimelineViewSet.as_view({'get': 'unlike_post'})),

     # comment event
     path('comment/<int:post_id>/', CommentViewSet.as_view({'get': 'list'})),
     path("comment/add/<int:post_id>", CommentViewSet.as_view({'post': 'create'}), name="new_comment"),
     path("comment/deleted/<int:comment_id>/", CommentViewSet.as_view({'get': 'destroy'}), name="update_post"),
     path('comment/like/<int:comment_id>/', CommentViewSet.as_view({'get': 'like_comment'})),
     path('comment/unlike/<int:comment_id>/', CommentViewSet.as_view({'get': 'unlike_comment'})),
]

