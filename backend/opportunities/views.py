from django.db.models import Q
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Opportunity
from .serializers import (
    OpportunityListSerializer,
    OpportunityDetailSerializer,
)


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
