from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.profile, name="profile"),
    # Experience
    path("experience/", views.experience, name="experience"),
    path("experience/add/", views.create_experience, name="create_experience"),
    path(
        "experience/add-ajax/",
        views.create_experience_ajax,
        name="create_experience_ajax",
    ),
    path(
        "experience/<uuid:experience_id>/edit/",
        views.update_experience,
        name="update_experience",
    ),
    path(
        "experience/<uuid:experience_id>/edit/ajax/",
        views.update_experience_ajax,
        name="update_experience_ajax",
    ),
    path(
        "experience/<uuid:experience_id>/delete/",
        views.delete_experience,
        name="delete_experience",
    ),
    path(
        "experience/<uuid:experience_id>/delete/ajax/",
        views.delete_experience_ajax,
        name="delete_experience_ajax",
    ),
    # Project
    path("projects/", views.projects, name="projects"),
    path("projects/add/", views.create_project, name="create_project"),
    path("projects/add-ajax/", views.create_project_ajax, name="create_project_ajax"),
    path("projects/<slug:slug>/edit/", views.update_project, name="update_project"),
    path(
        "projects/<slug:slug>/edit/",
        views.update_project_ajax,
        name="update_project_ajax",
    ),
    path(
        "projects/<uuid:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    path(
        "projects/<uuid:project_id>/delete/ajax/",
        views.delete_project_ajax,
        name="delete_project_ajax",
    ),
    path(
        "projects/<uuid:project_id>/star/",
        views.toggle_star,
        name="toggle_star",
    ),
    path(
        "projects/<uuid:project_id>/star/ajax/",
        views.toggle_star_ajax,
        name="toggle_star_ajax",
    ),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    # API
    path("api/projects/", views.get_projects_json, name="get_projects_json"),
    path(
        "api/projects/<slug:slug>/",
        views.get_project_detail_json,
        name="get_project_detail_json",
    ),
    path("api/experiences/", views.get_experiences_json, name="get_experiences_json"),
]
