
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers

from .models import Application
from opportunities.models import Opportunity
from profiles.models import Resume
from profiles.validators import validate_resume_file


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
            "full_name",
            "email",
            "phone",
            "course",
            "branch",
            "cgpa",
            "resume_title",
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
    # Choose an existing resume OR upload a new one.
    resume_id = serializers.IntegerField(write_only=True, required=False)
    new_resume = serializers.FileField(
        write_only=True, required=False, validators=[validate_resume_file]
    )

    class Meta:
        model = Application
        fields = (
            "id", "opportunity", "cover_letter",
            "full_name", "email", "phone", "course", "branch", "cgpa",
            "resume_id", "new_resume",
            "status", "applied_at",
        )
        read_only_fields = ("id", "status", "applied_at")
        extra_kwargs = {
            f: {"required": True, "allow_blank": False}
            for f in ("full_name", "email", "phone", "course", "branch")
        }
        extra_kwargs["cgpa"] = {"required": True, "allow_null": False}

    def validate(self, attrs):
        student = self.context["request"].user.student_profile
        resume_id = attrs.pop("resume_id", None)
        new_file = attrs.get("new_resume")

        if bool(resume_id) == bool(new_file):
            raise serializers.ValidationError(
                "Select an existing resume or upload a new one."
            )
        if resume_id:
            try:
                attrs["_resume"] = student.resumes.get(pk=resume_id)
            except Resume.DoesNotExist:
                raise serializers.ValidationError("Selected resume not found.")
        return attrs

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

    @transaction.atomic
    def create(self, validated_data):
        student = self.context["request"].user.student_profile
        new_file = validated_data.pop("new_resume", None)
        resume = validated_data.pop("_resume", None)

        if new_file:  # also keep it in the student's resume library
            resume = Resume.objects.create(
                student=student, title=new_file.name, file=new_file
            )

        application = Application(
            student=student, resume_title=resume.title, **validated_data
        )
        # Copy the file so the application keeps its own snapshot.
        with resume.file.open("rb") as f:
            application.resume.save(
                resume.file.name.split("/")[-1], ContentFile(f.read()), save=False
            )
        application.save()
        return application
