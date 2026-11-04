from rest_framework import serializers
from .models import Skill, StudentSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill

        fields = (
            "id",
            "name",
            "category",
        )

        read_only_fields = fields


class StudentSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)
    skill_category = serializers.CharField(source="skill.category", read_only=True)

    class Meta:
        model = StudentSkill

        fields = (
            "id",
            "skill",
            "skill_name",
            "skill_category",
            "proficiency",
            "created_at",
        )

        read_only_fields = (
            "id",
            "skill_name",
            "skill_category",
            "created_at",
        )

    def validate_skill(self, value):
        student = self.context["request"].user.student_profile

        existing = StudentSkill.objects.filter(student=student, skill=value)

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError("You have already added this skill.")

        return value
