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


class RecruiterOpportunitySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
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
            "company_name",
            "location",
            "work_mode",
            "openings",
            "compensation_min",
            "compensation_max",
            "compensation_period",
            "application_deadline",
            "status",
            "published_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "company_name",
            "status",
            "published_at",
            "created_at",
            "updated_at",
        )

    def validate_openings(self, value):
        if value < 1:
            raise serializers.ValidationError("There must be at least one opening.")
        return value

    def validate(self, attrs):
        minimum = attrs.get(
            "compensation_min",
            getattr(self.instance, "compensation_min", None),
        )
        maximum = attrs.get(
            "compensation_max",
            getattr(self.instance, "compensation_max", None),
        )

        if minimum is not None and maximum is not None and minimum > maximum:
            raise serializers.ValidationError(
                {
                    "compensation_max": "Maximum compensation cannot be lower than minimum compensation."
                }
            )

        return attrs
