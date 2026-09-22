import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import require_password
from .forms import ExperienceForm, ProjectForm
from .selectors import get_all_experiences_by_start_date, get_all_projects


# Create your views here.
def profile(req: HttpRequest) -> HttpResponse:
    last_login = req.COOKIES.get("last_login", "Belum ada sesi login")
    res = get_profile_json(req)
    ctx = {
        **json.loads(res.content.decode("utf-8")),
        "last_login": last_login,
    }

    return render(req, "home/profile.html", ctx)


# Experience
def experience(req: HttpRequest) -> HttpResponse:
    res = get_experiences_json(req)

    experiences = serializers.deserialize("json", res.content.decode("utf-8"))
    experiences = [exp.object for exp in experiences]

    ctx = {
        "experiences": experiences,
    }

    return render(req, "home/experience.html", ctx)


@require_password
def create_experience(req: HttpRequest) -> HttpResponse:
    form = ExperienceForm(req.POST or None)

    if req.method == "POST" and form.is_valid():
        form.save()
        messages.success(req, "Pengalaman baru berhasil ditambahkan!")
        return redirect("home:experience")

    ctx = {
        "form": form,
    }
    return render(req, "home/experience_form.html", ctx)


@require_password
def update_experience(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_object_or_404(
        get_all_experiences_by_start_date(), pk=experience_id
    )
    form = ExperienceForm(req.POST or None, instance=experience)

    if req.method == "POST" and form.is_valid():
        form.save()
        messages.success(req, "Pengalaman berhasil diperbarui!")
        return redirect("home:experience")

    ctx = {
        "form": form,
        "experience": experience,
    }
    return render(req, "home/experience_form.html", ctx)


@require_password
def delete_experience(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_object_or_404(
        get_all_experiences_by_start_date(), pk=experience_id
    )

    if req.method == "POST":
        experience.delete()
        messages.success(req, "Pengalaman berhasil dihapus!")
        return redirect("home:experience")

    return redirect("home:experience")


# Project
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
        "slug": slug,
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
def update_project(req: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(get_all_projects(), slug=slug)
    form = ProjectForm(req.POST or None, instance=project)

    if req.method == "POST" and form.is_valid():
        form.save()
        messages.success(req, "Proyek berhasil diperbarui!")
        return redirect("home:projects")

    ctx = {
        "form": form,
        "project": project,
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


# Auth
def register(req: HttpRequest) -> HttpResponse:
    form = UserCreationForm(req.POST or None)

    if req.method == "POST" and form.is_valid():
        user = form.save()
        login(req, user)
        messages.success(req, "Akun berhasil dibuat. Silakan login.")
        return redirect("home:login")

    ctx = {
        "form": form,
    }
    return render(req, "home/register.html", ctx)


def login_user(req: HttpRequest) -> HttpResponse:
    form = AuthenticationForm(req, data=req.POST or None)

    if req.method == "POST" and form.is_valid():
        user = form.get_user()
        login(req, user)
        res = redirect("home:profile")
        res.set_cookie(
            "last_login",
            datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
        )
        return res

    ctx = {
        "form": form,
    }
    return render(req, "home/login.html", ctx)


def logout_user(req: HttpRequest) -> HttpResponse:
    logout(req)
    res = redirect("home:profile")
    res.delete_cookie("last_login")
    return res


# API
def get_projects_json(req: HttpRequest) -> HttpResponse:
    title_query = req.GET.get("title", "").strip()
    projects = get_all_projects()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def get_project_detail_json(req: HttpRequest, slug: str) -> HttpResponse:
    project = get_object_or_404(get_all_projects(), slug=slug)

    project_json = serializers.serialize("json", [project])
    return HttpResponse(project_json, content_type="application/json")


def get_experiences_json(_req: HttpRequest) -> HttpResponse:
    experiences = get_all_experiences_by_start_date()

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def get_profile_json(_req: HttpRequest) -> HttpResponse:
    data = {
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

    return JsonResponse(data)
