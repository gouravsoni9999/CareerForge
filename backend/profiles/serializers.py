from rest_framework import serializers
from .models import StudentProfile, RecruiterProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = StudentProfile

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "college_name",
            "degree",
            "branch",
            "graduation_year",
            "cgpa",
            "bio",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
        )


class RecruiterProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
        default=None,
    )

    company_verification_status = serializers.CharField(
        source="company.verification_status",
        read_only=True,
        default=None,
    )

    class Meta:
        model = RecruiterProfile

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "company",
            "company_name",
            "company_verification_status",
            "phone_number",
            "designation",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "company",
            "company_name",
            "created_at",
            "updated_at",
        )
