from django.contrib import messages
from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import require_password
from .forms import ProjectForm
from .selectors import get_all_experiences_by_start_date, get_all_projects


# Create your views here.
def profile(req: HttpRequest) -> HttpResponse:
    ctx = {
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
        "experiences": get_all_experiences_by_start_date(),
    }

    return render(req, "home/experience.html", ctx)


def projects(req: HttpRequest) -> HttpResponse:
    res = get_projects_json(req)

    projects = serializers.deserialize("json", res.content.decode("utf-8"))
    projects = [project.object for project in projects]
    title_query = req.GET.get("title", "").strip()

    ctx = {
        "projects": projects,
        "title_query": title_query,
    }

    return render(req, "home/projects.html", ctx)


def project_detail(req: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(get_all_projects(), slug=slug)

    ctx = {
        "project": project,
    }

    return render(req, "home/project_detail.html", ctx)


@require_password
def create_project(req: HttpRequest) -> HttpResponse:
    form = ProjectForm(req.POST or None)

    if req.method == "POST" and form.is_valid():
        form.save()
        messages.success(req, "Proyek baru berhasil ditambahkan!")
        return redirect("home:projects")

    ctx = {
        "form": form,
    }
    return render(req, "home/project_form.html", ctx)


@require_password
def delete_project(req: HttpRequest, project_id: int) -> HttpResponse:
    project = get_object_or_404(get_all_projects(), pk=project_id)

    if req.method == "POST":
        project.delete()
        messages.success(req, "Project berhasil dihapus!")
        return redirect("home:projects")

    return redirect("home:projects")


# API


def get_projects_json(req: HttpRequest) -> HttpResponse:
    title_query = req.GET.get("title", "").strip()
    projects = get_all_projects()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")
