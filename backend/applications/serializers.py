
from django.utils import timezone

from rest_framework import serializers

from .models import Application
from opportunities.models import Opportunity


class ApplicationSerializer(serializers.ModelSerializer):
    opportunity_title = serializers.CharField(
        source="opportunity.title",
        read_only=True,
    )
    company_name = serializers.CharField(
        source="opportunity.company.name",
        read_only=True,
    )
    opportunity_type = serializers.CharField(
        source="opportunity.opportunity_type",
        read_only=True,
    )
    opportunity_location = serializers.CharField(
        source="opportunity.location",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "opportunity",
            "opportunity_title",
            "company_name",
            "opportunity_type",
            "opportunity_location",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "applied_at",
            "updated_at",
        )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id",
            "opportunity",
            "cover_letter",
            "status",
            "applied_at",
        )
        read_only_fields = (
            "id",
            "status",
            "applied_at",
        )

    def validate_opportunity(self, opportunity):
        today = timezone.localdate()

        if opportunity.status != Opportunity.OpportunityStatus.PUBLISHED:
            raise serializers.ValidationError(
                "This opportunity is not currently accepting applications."
            )

        if (
            opportunity.company.verification_status
            != "VERIFIED"
        ):
            raise serializers.ValidationError(
                "This company's verification is pending."
            )

        if opportunity.application_deadline < today:
            raise serializers.ValidationError(
                "The application deadline has passed."
            )

        student = self.context["request"].user.student_profile

        if Application.objects.filter(
            student=student,
            opportunity=opportunity,
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this opportunity."
            )

        return opportunity

    def create(self, validated_data):
        student = self.context["request"].user.student_profile

        return Application.objects.create(
            student=student,
            **validated_data,
        )