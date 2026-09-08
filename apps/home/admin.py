from django.contrib import admin

from .models import Experience, Project


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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "project_url")

    list_filter = ("category",)

    search_fields = ("title", "description")

    ordering = ("title",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("title", "category", "thumbnail", "description"),
            },
        ),
        (
            "Details",
            {
                "fields": ("technologies", "project_url"),
            },
        ),
    )
