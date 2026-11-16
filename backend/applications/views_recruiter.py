
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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


class RecruiterApplicationResumeView(APIView):
    """Streams the applicant's resume; ?download=1 forces a download."""

    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, pk):
        application = get_object_or_404(
            Application,
            pk=pk,
            opportunity__posted_by=request.user.recruiter_profile,
        )
        if not application.resume:
            from rest_framework.exceptions import NotFound
            raise NotFound("No resume attached.")

        name = f"{application.full_name or 'resume'}-resume.pdf".replace(" ", "_")
        return FileResponse(
            application.resume.open("rb"),
            content_type="application/pdf",
            as_attachment=request.query_params.get("download") == "1",
            filename=name,
        )
