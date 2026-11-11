from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "industry",
        "location",
        "verification_status",
        "created_at",
    )

    search_fields = ("name", "industry", "location")
    list_filter = ("verification_status", "industry")
    readonly_fields = ("created_at", "updated_at")

    actions = ("verify_companies", "reject_companies")

    @admin.action(description="Approve selected companies")
    def verify_companies(self, request, queryset):
        updated = queryset.update(
            verification_status=Company.VerificationStatus.VERIFIED
        )
        self.message_user(
            request,
            f"{updated} company registration(s) approved.",
        )

    @admin.action(description="Reject selected companies")
    def reject_companies(self, request, queryset):
        updated = queryset.update(
            verification_status=Company.VerificationStatus.REJECTED
        )
        self.message_user(
            request,
            f"{updated} company registration(s) rejected.",
        )