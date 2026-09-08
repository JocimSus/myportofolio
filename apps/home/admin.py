from django.contrib import admin

from .models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "end_date", "is_ongoing")

    list_filter = ("category", "start_date")

    search_fields = ("title", "description")

    ordering = ("start_date",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("title", "category", "thumbnail", "description"),
            },
        ),
        (
            "Timeline",
            {
                "fields": ("start_date", "end_date"),
            },
        ),
    )
