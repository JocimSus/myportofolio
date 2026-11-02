import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import ExperienceForm, ProjectForm
from .selectors import (
    get_all_experiences_by_start_date,
    get_experience_by_id,
    get_experiences_dict,
    get_profile_data,
    get_project_by_id,
    get_project_by_slug,
    get_project_by_slug_dict,
    get_projects_with_stars,
)


def _is_htmx(request: HttpRequest) -> bool:
    return request.headers.get("HX-Request") == "true"


def profile(req: HttpRequest) -> HttpResponse:
    last_login = req.COOKIES.get("last_login", "Belum ada sesi login")
    res = get_profile_data()
    ctx = {
        **res,
        "last_login": last_login,
    }

    return render(req, "home/profile.html", ctx)


# Experience
def experience(req: HttpRequest) -> HttpResponse:
    ctx = {
        "form": ExperienceForm(),
        "experiences": get_all_experiences_by_start_date(),
    }
    return render(req, "home/experience.html", ctx)


@login_required(login_url="/login/")
@permission_required("home.add_experience", raise_exception=True)
def experience_form_fragment(req: HttpRequest) -> HttpResponse:
    return render(
        req,
        "home/partials/experience_form.html",
        {"form": ExperienceForm(), "mode": "create"},
    )


@login_required(login_url="/login/")
@permission_required("home.change_experience", raise_exception=True)
def experience_edit_fragment(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_experience_by_id(experience_id)
    return render(
        req,
        "home/partials/experience_form.html",
        {
            "form": ExperienceForm(instance=experience),
            "experience": experience,
            "mode": "update",
        },
    )


@login_required(login_url="/login/")
@permission_required("home.add_experience", raise_exception=True)
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


@login_required(login_url="/login/")
@require_POST
@permission_required("home.add_experience", raise_exception=True)
def create_experience_ajax(request):
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        if _is_htmx(request):
            return render(
                request,
                "home/partials/experience_response.html",
                {"experiences": get_all_experiences_by_start_date()},
            )
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    if _is_htmx(request):
        response = render(
            request,
            "home/partials/experience_form.html",
            {"form": form, "mode": "create"},
        )
        response["HX-Retarget"] = "#experience-form-container"
        response["HX-Reswap"] = "innerHTML"
        return response

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@permission_required("home.change_experience", raise_exception=True)
def update_experience(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_experience_by_id(experience_id)
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


@login_required(login_url="/login/")
@require_http_methods(["POST", "PUT"])
@permission_required("home.change_experience", raise_exception=True)
def update_experience_ajax(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_experience_by_id(experience_id)
    form_data = req.POST if req.method == "POST" else QueryDict(req.body)
    form = ExperienceForm(form_data, instance=experience)

    if form.is_valid():
        form.save()
        if _is_htmx(req):
            return render(
                req,
                "home/partials/experience_response.html",
                {"experiences": get_all_experiences_by_start_date()},
            )
        return JsonResponse({"message": "Pengalaman berhasil diperbarui."}, status=200)

    if _is_htmx(req):
        response = render(
            req,
            "home/partials/experience_form.html",
            {"form": form, "experience": experience, "mode": "update"},
        )
        response["HX-Retarget"] = "#experience-form-container"
        response["HX-Reswap"] = "innerHTML"
        return response

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@permission_required("home.delete_experience", raise_exception=True)
def delete_experience(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_experience_by_id(experience_id)

    if req.method == "POST":
        experience.delete()
        messages.success(req, "Pengalaman berhasil dihapus!")
        return redirect("home:experience")

    return redirect("home:experience")


@login_required(login_url="/login/")
@require_http_methods(["POST", "DELETE"])
@permission_required("home.delete_experience", raise_exception=True)
def delete_experience_ajax(req: HttpRequest, experience_id: str) -> HttpResponse:
    experience = get_experience_by_id(experience_id)
    experience.delete()
    if _is_htmx(req):
        if get_all_experiences_by_start_date().exists():
            return HttpResponse("")
        return render(req, "home/partials/experience_list.html", {"experiences": []})
    return JsonResponse({"message": "Pengalaman berhasil dihapus."}, status=200)


# Project
def projects(req: HttpRequest) -> HttpResponse:
    title_query = req.GET.get("title", "").strip()

    ctx = {
        "title_query": title_query,
        "form": ProjectForm(),
        "projects": get_projects_with_stars(title_query=title_query, user=req.user),
    }
    if _is_htmx(req):
        return render(req, "home/partials/project_cards.html", ctx)
    return render(req, "home/projects.html", ctx)


def project_detail(req: HttpRequest, slug: str) -> HttpResponse:
    project = get_project_by_slug(slug)
    ctx = {
        "slug": slug,
        "project": project,
        "form": ProjectForm(),
    }
    return render(req, "home/project_detail.html", ctx)


@login_required(login_url="/login/")
@permission_required("home.add_project", raise_exception=True)
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


@login_required(login_url="/login/")
@require_POST
@permission_required("home.add_project", raise_exception=True)
def create_project_ajax(request):
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        if _is_htmx(request):
            return render(
                request,
                "home/partials/project_cards.html",
                {"projects": get_projects_with_stars(user=request.user)},
            )
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    if _is_htmx(request):
        response = render(
            request,
            "home/partials/project_form_fields.html",
            {"form": form},
        )
        response["HX-Retarget"] = "#project-form-fields"
        response["HX-Reswap"] = "innerHTML"
        return response

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@permission_required("home.change_project", raise_exception=True)
def update_project(req: HttpRequest, slug: str) -> HttpResponse:
    project = get_project_by_slug(slug)
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


@login_required(login_url="/login/")
@require_POST
@permission_required("home.change_project", raise_exception=True)
def update_project_ajax(req: HttpRequest, slug: str) -> JsonResponse:
    project = get_project_by_slug(slug)
    form = ProjectForm(req.POST, instance=project)

    if form.is_valid():
        form.save()
        return JsonResponse({"message": "Proyek berhasil diperbarui."}, status=200)

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
@permission_required("home.delete_project", raise_exception=True)
def delete_project(req: HttpRequest, project_id: int) -> HttpResponse:
    project = get_project_by_id(project_id)

    if req.method == "POST":
        project.delete()
        messages.success(req, "Project berhasil dihapus!")
        return redirect("home:projects")

    return redirect("home:projects")


@login_required(login_url="/login/")
@require_http_methods(["POST", "DELETE"])
@permission_required("home.delete_project", raise_exception=True)
def delete_project_ajax(req: HttpRequest, project_id: int) -> HttpResponse:
    project = get_project_by_id(project_id)
    project.delete()
    if _is_htmx(req):
        form_data = req.POST if req.method == "POST" else QueryDict(req.body)
        title_query = form_data.get("title", "").strip()
        projects = get_projects_with_stars(title_query=title_query, user=req.user)
        if projects:
            return HttpResponse("")
        return render(req, "home/partials/project_cards.html", {"projects": projects})
    return JsonResponse({"message": "Proyek berhasil dihapus."}, status=200)


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_project_by_id(project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("home:projects")


@login_required(login_url="/login/")
@require_POST
def toggle_star_ajax(request, project_id):
    project = get_project_by_id(project_id)

    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
        is_starred = False
    else:
        project.starred_by.add(request.user)
        is_starred = True

    return JsonResponse(
        {
            "message": "Proyek berhasil diberi bintang.",
            "is_starred": is_starred,
            "star_count": project.starred_by.count(),
        }
    )


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


@login_required(login_url="/login/")
def logout_user(req: HttpRequest) -> HttpResponse:
    logout(req)
    res = redirect("home:profile")
    res.delete_cookie("last_login")
    return res


# API
def get_projects_json(req: HttpRequest) -> JsonResponse:
    title_query = req.GET.get("title", "").strip()

    projects_data = get_projects_with_stars(title_query=title_query, user=req.user)
    return JsonResponse(projects_data, safe=False)


def get_project_detail_json(_req: HttpRequest, slug: str) -> JsonResponse:
    project = get_project_by_slug_dict(slug)

    return JsonResponse(project)


def get_experiences_json(_req: HttpRequest) -> JsonResponse:
    experiences = get_experiences_dict()

    return JsonResponse(experiences, safe=False)
