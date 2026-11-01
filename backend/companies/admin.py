from django.contrib import admin
from .models import Company

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry","location", "verification_status", "created_at",)
    search_fields = ("name", "industry", "location",)
    list_filter = ("verification_status", "industry",)
    readonly_fields = ("created_at", "updated_at",)