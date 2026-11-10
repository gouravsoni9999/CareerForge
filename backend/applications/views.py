
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsStudent

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
)


class StudentApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return (
            Application.objects.filter(
                student=self.request.user.student_profile
            )
            .select_related(
                "opportunity",
                "opportunity__company",
            )
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ApplicationCreateSerializer

        return ApplicationSerializer


class StudentApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Application.objects.filter(
            student=self.request.user.student_profile
        ).select_related(
            "opportunity",
            "opportunity__company",
        )


class StudentApplicationWithdrawView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, pk):
        application = get_object_or_404(
            Application,
            pk=pk,
            student=request.user.student_profile,
        )

        if application.status in [
            Application.ApplicationStatus.SELECTED,
            Application.ApplicationStatus.REJECTED,
            Application.ApplicationStatus.WITHDRAWN,
        ]:
            return Response(
                {"detail": "This application cannot be withdrawn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Application.ApplicationStatus.WITHDRAWN
        application.save(update_fields=["status", "updated_at"])

        return Response(
            {
                "message": "Application withdrawn successfully.",
                "application": ApplicationSerializer(application).data,
            },
            status=status.HTTP_200_OK,
        )