import uuid
from typing import ClassVar

from django.db import models


class Experience(models.Model):
    EXPERIENCE_TYPE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
        ("competition", "Competition"),
        ("organization", "Organization"),
        ("committee", "Committee"),
        ("community", "Community"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES)
    thumbnail = models.URLField(max_length=200, null=True, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.end_date is None

    @property
    def get_category_display(self):
        return dict(self.EXPERIENCE_TYPE_CHOICES).get(self.experience_type, "Unknown")
