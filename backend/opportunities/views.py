from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .models import Opportunity
from .serializers import (
    OpportunityListSerializer,
    OpportunityDetailSerializer,
    RecruiterOpportunitySerializer,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsRecruiter
from applications.models import Application
from applications.serializers_recruiter import RecruiterApplicantSerializer


class OpportunityListView(generics.ListAPIView):

    serializer_class = OpportunityListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        today = timezone.localdate()

        queryset = (
            Opportunity.objects.filter(
                status="PUBLISHED",
                company__verification_status="VERIFIED",
            )
            .filter(
                Q(application_deadline__isnull=True)
                | Q(application_deadline__gte=today)
            )
            .select_related(
                "company",
            )
        )

        params = self.request.query_params

        # Search by title, company name or description.
        search = params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(company__name__icontains=search)
                | Q(description__icontains=search)
            )

        # Filter by opportunity type.
        opportunity_type = params.get("type")

        if opportunity_type:
            queryset = queryset.filter(opportunity_type__iexact=opportunity_type)

        # Filter by location.
        location = params.get("location")

        if location:
            queryset = queryset.filter(location__icontains=location)

        # Filter by work mode.
        work_mode = params.get("work_mode")

        if work_mode:
            queryset = queryset.filter(work_mode__iexact=work_mode)

        # Minimum compensation requested by the student.
        min_compensation = params.get("min_compensation")

        if min_compensation:
            try:
                min_value = float(min_compensation)
                queryset = queryset.filter(
                    Q(compensation_max__gte=min_value)
                    | Q(compensation_max__isnull=True)
                )
            except ValueError:
                pass

        # Maximum compensation requested by the student.
        max_compensation = params.get("max_compensation")

        if max_compensation:
            try:
                max_value = float(max_compensation)
                queryset = queryset.filter(
                    Q(compensation_min__lte=max_value)
                    | Q(compensation_min__isnull=True)
                )
            except ValueError:
                pass

        # Allow only approved ordering fields.
        ordering = params.get("ordering", "-published_at")

        allowed_ordering = {
            "published_at",
            "-published_at",
            "application_deadline",
            "-application_deadline",
            "compensation_min",
            "-compensation_min",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class OpportunityDetailView(generics.RetrieveAPIView):

    serializer_class = OpportunityDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        today = timezone.localdate()

        return (
            Opportunity.objects.filter(
                status="PUBLISHED",
                company__verification_status="VERIFIED",
            )
            .filter(
                Q(application_deadline__isnull=True)
                | Q(application_deadline__gte=today)
            )
            .select_related(
                "company",
            )
        )


class RecruiterOpportunityListCreateView(generics.ListCreateAPIView):
    serializer_class = RecruiterOpportunitySerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        return Opportunity.objects.filter(
            posted_by=self.request.user.recruiter_profile
        ).select_related("company", "posted_by")

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter_profile

        if not recruiter.company:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                "Register a company before creating opportunities."
            )

        if recruiter.company.verification_status != "VERIFIED":
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                "Your company must be verified before creating opportunities."
            )

        serializer.save(
            company=recruiter.company,
            posted_by=recruiter,
        )


class RecruiterOpportunityDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterOpportunitySerializer
    permission_classes = [IsAuthenticated, IsRecruiter]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Opportunity.objects.filter(
            posted_by=self.request.user.recruiter_profile
        ).select_related("company", "posted_by")


class PublishOpportunityView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def post(self, request, pk):
        recruiter = request.user.recruiter_profile

        opportunity = get_object_or_404(
            Opportunity,
            pk=pk,
            posted_by=recruiter,
        )

        if not recruiter.company or recruiter.company.verification_status != "VERIFIED":
            return Response(
                {"detail": "Your company must be verified before publishing."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if opportunity.status != Opportunity.OpportunityStatus.DRAFT:
            return Response(
                {"detail": "Only draft opportunities can be published."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if opportunity.application_deadline < timezone.localdate():
            return Response(
                {"detail": "The application deadline has already passed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        opportunity.status = Opportunity.OpportunityStatus.PUBLISHED
        opportunity.published_at = timezone.now()
        opportunity.save(update_fields=["status", "published_at", "updated_at"])

        return Response(
            RecruiterOpportunitySerializer(opportunity).data,
            status=status.HTTP_200_OK,
        )


class RecruiterOpportunityApplicationsView(generics.ListAPIView):
    serializer_class = RecruiterApplicantSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        recruiter = self.request.user.recruiter_profile

        return Application.objects.filter(
            opportunity__posted_by=recruiter,
            opportunity_id=self.kwargs["pk"],
        ).select_related(
            "student",
            "student__user",
            "opportunity",
            "opportunity__company",
        )
