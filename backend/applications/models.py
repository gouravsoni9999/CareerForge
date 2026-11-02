from django.db import models

# Create your models here.
class Application(models.Model):
    class ApplicationStatus(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED", "Interview Scheduled"
        SELECTED = "SELECTED", "Selected"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    # Student who submitted the application
    student = models.ForeignKey(
        "profiles.StudentProfile",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    # Opportunity for which the student applied
    opportunity = models.ForeignKey(
        "opportunities.Opportunity",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    # Application Details
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.APPLIED)

    # Internal notes for recruiters/admin
    recruiter_notes = models.TextField(blank=True)

    # timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "opportunity"],
                name="unique_student_opportunity_application",
            ),
        ]

        indexes = [
            models.Index(
                fields=["status", "applied_at"],
                name="app_status_applied_idx",
            ),
            models.Index(
                fields=["opportunity", "status"],
                name="app_opp_status_idx",
            ),
        ]     

    def __str__(self):
        return (
            f"{self.student.user.email} -> "
            f"{self.opportunity.title} ({self.status})"
        )                   