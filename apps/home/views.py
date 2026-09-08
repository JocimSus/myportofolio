from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .selectors import get_all_experiences_by_start_date, get_all_projects


# Create your views here.
def profile(req: HttpRequest) -> HttpResponse:
    ctx = {
        "name": "Joachim Susatiyo",
        "nick": "Joachim",
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

    return render(req, "home/profile.html", ctx)


def experience(req: HttpRequest) -> HttpResponse:
    ctx = {
        "name": "Joachim Susatiyo",
        "nick": "Joachim",
        "experiences": get_all_experiences_by_start_date(),
    }

    return render(req, "home/experience.html", ctx)


def projects(req: HttpRequest) -> HttpResponse:
    ctx = {
        "projects": get_all_projects(),
    }

    return render(req, "home/projects.html", ctx)
