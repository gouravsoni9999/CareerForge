from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsRecruiter
from .models import Company
from .serializers import (
    CompanyCreateSerializer,
    CompanySerializer,
)


# Create your views here.
class CompanyListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(
            verification_status=Company.VerificationStatus.VERIFIED
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CompanyCreateSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsRecruiter()]
        return [permission() for permission in self.permission_classes]


class CompanyDetailView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(
            verification_status=Company.VerificationStatus.VERIFIED
        )