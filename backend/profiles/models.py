from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_resume_file
from django.db.models import Q


# Create your models here.
class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    college_name = models.CharField(
        max_length=255,
        blank=True,
    )

    degree = models.CharField(
        max_length=100,
        blank=True,
    )

    branch = models.CharField(
        max_length=100,
        blank=True,
    )

    graduation_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )

    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student profile: {self.user.email}"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recruiters",
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recruiter profile: {self.user.email}"


class Resume(models.Model):
    student = models.ForeignKey(
        "profiles.StudentProfile", on_delete=models.CASCADE, related_name="resumes"
    )

    title = models.CharField(
        max_length=150,
        default="My Resume",
    )

    file = models.FileField(
        upload_to="resumes/%Y/%m/",
        validators=[validate_resume_file],
    )

    is_primary = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["student"],
                condition=Q(is_primary=True),
                name="unique_primary_resume_per_student",
            ),
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.title}"