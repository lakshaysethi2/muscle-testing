from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "display_name",
        "testing_method",
        "karma",
        "is_staff",
        "date_joined",
    )
    list_filter = ("testing_method", "is_staff", "is_superuser", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name", "bio")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("TruthCheck Profile", {"fields": ("bio", "testing_method", "karma")}),
    )
