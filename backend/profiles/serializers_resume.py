from django.db import transaction
from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume

        fields = (
            "id", "title", "file", "is_primary", "uploaded_at", "updated_at",
        )

        read_only_fields = ("id", "uploaded_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        student = self.context["request"].user.student_profile

        if validated_data.get("is_primary", False):
            Resume.objects.filter(student = student, is_primary = True).update(is_primary = False)

        return Resume.objects.create(
            student = student, **validated_data
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get("is_primary") is True:
            Resume.objects.filter(student = instance.student, is_primary = True).exclude(pk = instance.pk).update(is_primary = False)

        return super().update(instance, validated_data)
