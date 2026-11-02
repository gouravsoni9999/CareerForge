from django.contrib import admin
from .models import StudentProfile, RecruiterProfile, Resume


# Register your models here.
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "college_name",
        "branch",
        "graduation_year",
        "cgpa",
    )

    search_fields = (
        "user__email",
        "college_name",
        "branch",
    )

    list_filter = (
        "graduation_year",
        "branch",
    )


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "designation",
        "phone_number",
    )

    search_fields = ("user__email", "company__name", "designation")
    list_filter = ("company",)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "title",
        "is_primary",
        "uploaded_at",
    )

    search_fields = (
        "student__user__email",
        "title",
    )

    list_filter = (
        "is_primary",
        "uploaded_at",
    )

    readonly_fields = (
        "uploaded_at",
        "updated_at",
    )

    autocomplete_fields = (
        "student",
    )