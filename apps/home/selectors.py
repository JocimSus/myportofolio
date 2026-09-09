from django.db.models import QuerySet

from .models import Experience, Project


def get_all_experiences_by_start_date() -> QuerySet[Experience]:
    return Experience.objects.order_by("start_date")


def get_all_projects() -> QuerySet[Project]:
    return Project.objects.all()
