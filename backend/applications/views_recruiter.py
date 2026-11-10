
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsRecruiter

from .models import Application
from .serializers_recruiter import RecruiterApplicationStatusSerializer


class RecruiterApplicationStatusView(generics.UpdateAPIView):
    serializer_class = RecruiterApplicationStatusSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    http_method_names = ["patch", "options", "head"]

    def get_queryset(self):
        return Application.objects.filter(
            opportunity__posted_by=self.request.user.recruiter_profile
        ).select_related(
            "student",
            "student__user",
            "opportunity",
        )