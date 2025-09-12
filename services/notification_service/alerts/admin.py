from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("title", "message", "user__username")
    readonly_fields = ("created_at",)