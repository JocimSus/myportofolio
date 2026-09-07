import uuid

from django.db import models

from .choices import ExperienceType


class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ExperienceType.choices)
    thumbnail = models.URLField(max_length=200, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @property
    def is_ongoing(self) -> bool:
        return self.end_date is None

    @property
    def get_category_display(self) -> str:
        try:
            return str(ExperienceType(self.category).label)
        except ValueError:
            return "Unknown"
