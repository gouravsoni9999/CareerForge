from rest_framework import serializers

from .models import Opportunity


class OpportunityListSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    company_location = serializers.CharField(
        source="company.location",
        read_only=True,
    )

    class Meta:
        model = Opportunity

        fields = (
            "id",
            "title",
            "opportunity_type",
            "company",
            "company_name",
            "company_location",
            "location",
            "work_mode",
            "openings",
            "compensation_min",
            "compensation_max",
            "compensation_period",
            "application_deadline",
            "published_at",
        )


class OpportunityDetailSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    company_location = serializers.CharField(
        source="company.location",
        read_only=True,
    )

    company_website = serializers.CharField(
        source="company.website",
        read_only=True,
    )

    class Meta:
        model = Opportunity

        fields = (
            "id",
            "title",
            "opportunity_type",
            "description",
            "responsibilities",
            "requirements",
            "eligibility_criteria",
            "company",
            "company_name",
            "company_location",
            "company_website",
            "location",
            "work_mode",
            "openings",
            "compensation_min",
            "compensation_max",
            "compensation_period",
            "application_deadline",
            "published_at",
            "created_at",
            "updated_at",
        )