from django.db import transaction
from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    # used to display company info
    class Meta:
        model = Company

        fields = (
            "id",
            "name",
            "website",
            "industry",
            "description",
            "location",
            "verification_status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "verification_status",
            "updated_at",
            "created_at",
        )


class CompanyCreateSerializer(serializers.ModelSerializer):
    # used when recruiter submits a company
    class Meta:
        model = Company

        fields = (
            "id",
            "name",
            "website",
            "industry",
            "description",
            "location",
            "verification_status",
            "created_at",
        )

        read_only_fields = (
            "id",
            "verification_status",
            "created_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if Company.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A company with this name already exists."
            )
        return value

    def validate(self, attrs):
        recruiter = self.context["request"].user.recruiter_profile

        if recruiter.company_id is not None:
            raise serializers.ValidationError(
                "You are already associated with a company."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        recruiter = self.context["request"].user.recruiter_profile
        company = Company.objects.create(**validated_data)
        recruiter.company = company
        recruiter.save(update_fields=["company"])
        return company
