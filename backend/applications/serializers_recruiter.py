
from rest_framework import serializers

from .models import Application


class RecruiterApplicantSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()

    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = (
            "id",
            "student_name",
            "student_email",
            "phone",
            "course",
            "branch",
            "cgpa",
            "cover_letter",
            "resume_title",
            "resume_url",
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
        return obj.full_name or obj.student.user.get_full_name()

    def get_student_email(self, obj):
        return obj.email or obj.student.user.email

    def get_resume_url(self, obj):
        return f"/api/applications/recruiter/{obj.pk}/resume/" if obj.resume else None


class RecruiterApplicationStatusSerializer(RecruiterApplicantSerializer):
    class Meta(RecruiterApplicantSerializer.Meta):
        read_only_fields = tuple(
            f for f in RecruiterApplicantSerializer.Meta.fields
            if f not in ("status", "recruiter_notes")
        )

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
