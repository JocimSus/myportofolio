from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Experience, Project


def get_all_experiences_by_start_date() -> QuerySet[Experience]:
    return Experience.objects.order_by("start_date")


def get_experience_by_id(experience_id: str) -> Experience:
    return get_object_or_404(get_all_experiences_by_start_date(), pk=experience_id)


def get_all_projects() -> QuerySet[Project]:
    return Project.objects.all()


def get_projects(title_query: str = "") -> QuerySet[Project]:
    projects = get_all_projects()
    if title_query:
        return projects.filter(title__icontains=title_query)
    return projects


def get_project_by_slug(slug: str) -> Project:
    return get_object_or_404(get_all_projects(), slug=slug)


def get_project_by_id(project_id) -> Project:
    return get_object_or_404(get_all_projects(), pk=project_id)


def get_profile_data() -> dict:
    return {
        "npm": "2506602694",
        "study_program": "Ilmu Komputer - S1",
        "bio": (
            "a passionate computer science student at Universitas Indonesia. "
            "I love exploring new technologies and applying them to solve real-world problems."
        ),
        "interests": [
            "Web Development",
            "System Design",
            "Operating Systems",
            "Cloud Infrastructure",
            "Web Development",
        ],
        "experience_truncated": [
            "Winner of RISTEK Hackathon 2026",
            "Vice Lead of IT Dev OH Fasilkom 2026",
            "Member of RISTEK Web Development",
        ],
    }


def get_default_context() -> dict:
    return {
        "name": "Joachim Susatiyo",
        "nick": "Joachim",
    }
