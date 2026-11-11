
from rest_framework import serializers

from .models import Application


class RecruiterApplicantSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.EmailField(
        source="student.user.email",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "student_name",
            "student_email",
            "status",
            "recruiter_notes",
            "applied_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "student_name",
            "student_email",
            "applied_at",
            "updated_at",
        )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()


class RecruiterApplicationStatusSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.EmailField(
        source="student.user.email",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "student_name",
            "student_email",
            "status",
            "recruiter_notes",
            "applied_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "student_name",
            "student_email",
            "applied_at",
            "updated_at",
        )

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()

    def validate_status(self, value):
        allowed_statuses = [
            Application.ApplicationStatus.UNDER_REVIEW,
            Application.ApplicationStatus.SHORTLISTED,
            Application.ApplicationStatus.INTERVIEW_SCHEDULED,
            Application.ApplicationStatus.SELECTED,
            Application.ApplicationStatus.REJECTED,
        ]

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                "This status cannot be assigned by a recruiter."
            )

        return value
