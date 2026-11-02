from django.contrib import admin
from .models import Application


# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "opportunity",
        "status",
        "applied_at",
        "updated_at",
    )

    search_fields = (
        "student__user__email",
        "opportunity__title",
        "opportunity__company__name",
    )

    list_filter = (
        "status",
        "opportunity__opportunity_type",
        "applied_at",
    )

    readonly_fields = (
        "applied_at",
        "updated_at",
    )

    autocomplete_fields = (
        "student",
        "opportunity",
    )

    date_hierarchy = "applied_at"

    