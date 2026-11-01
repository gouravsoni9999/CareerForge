from django.contrib import admin
from .models import StudentProfile, RecruiterProfile

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
        "user_email",
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
        "user", "company" , "designation", "phone_number",
    )

    search_fields = ("user__email","company__email", "designation")
    list_filter = ("company",)
