from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


# Create your models here.
class Opportunity(models.Model):
    class OpportunityType(models.TextChoices):
        INTERNSHIP = "INTERNSHIP", "Internship"
        FULL_TIME = "FULL_TIME", "Full-time Job"

    class WorkMode(models.TextChoices):
        ONSITE = "ONSITE", "On-site"
        REMOTE = "REMOTE", "Remote"
        HYBRID = "HYBRID", "Hybrid"

    class OpportunityStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"
        EXPIRED = "EXPIRED", "Expired"

    # Basic Info
    title = models.CharField(max_length=255)

    opportunity_type = models.CharField(
        max_length=20,
        choices=OpportunityType.choices,
    )
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    eligibility_criteria = models.TextField(blank=True)

    # Company and recruiter
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT,
        related_name="opportunities",
    )

    posted_by = models.ForeignKey(
        "profiles.RecruiterProfile",
        on_delete=models.PROTECT,
        related_name="posted_opportunities",
    )

    # Work Details
    location = models.CharField(max_length=255, blank=True)
    work_mode = models.CharField(
        max_length=20, choices=WorkMode.choices, default=WorkMode.ONSITE
    )
    openings = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator]
    )

    # Compensation(INR)
    compensation_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    compensation_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    compensation_period = models.CharField(
        max_length=20,
        blank=True,
        help_text="Examples: monthly, yearly, one-time.",
    )

    # Dates and Status
    application_deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=OpportunityStatus.choices,
        default=OpportunityStatus.DRAFT,
    )

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "application_deadline"],
                name="opp_status_deadline_idx",
            ),
            models.Index(
                fields=["opportunity_type", "work_mode"],
                name="opp_type_workmode_idx",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    @property
    def is_application_open(self):
        return (
            self.status == self.OpportunityStatus.PUBLISHED
            and self.application_deadline >= timezone.localdate()
        )
