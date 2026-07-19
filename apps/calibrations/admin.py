from django.contrib import admin

from .models import Calibration


@admin.register(Calibration)
class CalibrationAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "submitter_name",
        "result",
        "calibration_level",
        "method",
        "category",
        "visibility",
        "verification_count",
        "flag_count",
        "created_at",
    )
    list_filter = ("result", "category", "visibility", "method", "is_removed")
    search_fields = ("subject", "notes", "user__username", "user__email")
    readonly_fields = ("verification_count", "flag_count", "created_at", "updated_at")
    actions = ["mark_removed", "approve_entry"]
    ordering = ["-created_at"]

    @admin.action(description="Mark selected as removed (soft-delete)")
    def mark_removed(self, request, queryset):
        queryset.update(is_removed=True, visibility=Calibration.Visibility.PRIVATE)

    @admin.action(description="Approve selected (unflag, set public)")
    def approve_entry(self, request, queryset):
        queryset.update(
            is_removed=False, flag_count=0, visibility=Calibration.Visibility.PUBLIC
        )
