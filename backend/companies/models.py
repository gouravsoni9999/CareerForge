from django.db import models

# Create your models here.
class Company(models.Model):

    class VerificationStatus(models.TextChoices):
        PENDING = "PENDING","Pending"
        VERIFIED = "VERIFIED","Verified"
        REJECTED = "REJECTED", "Rejected"

    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name