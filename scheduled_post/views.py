from rest_framework import viewsets, permissions
from .models import ScheduledPost
from .serializers import ScheduledPostSerializer


class ScheduledPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ScheduledPost.objects.all()
    serializer_class = ScheduledPostSerializer
