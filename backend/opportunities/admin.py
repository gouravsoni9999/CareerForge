from django.contrib import admin
from .models import Opportunity


# Register your models here.
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "opportunity_type",
        "work_mode",
        "status",
        "application_deadline",
        "created_at",
    )

    search_fields = (
        "title",
        "company__name",
        "posted_by__user__email",
    )

    list_filter = (
        "opportunity_type",
        "work_mode",
        "status",
        "application_deadline",
    )

    readonly_fields = (
        "published_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "company",
        "posted_by",
    )

    date_hierarchy = "created_at"