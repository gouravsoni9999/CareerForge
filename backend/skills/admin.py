from django.contrib import admin
from .models import StudentSkill, Skill

# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "category",
    )

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "skill",
        "proficiency",
        "created_at",
    )

    search_fields = (
        "student__user__email",
        "skill__name",
    )

    list_filter = (
        "proficiency",
        "skill__category",
    )

    autocomplete_fields = (
        "student",
        "skill",
    )