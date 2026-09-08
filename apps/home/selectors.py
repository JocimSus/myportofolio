from django.db.models import QuerySet

from .models import Experience


def get_all_experiences_by_start_date() -> QuerySet[Experience]:
    return Experience.objects.order_by("start_date")
