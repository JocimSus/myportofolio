from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.profile, name="profile"),
    # Experience
    path("experience/", views.experience, name="experience"),
    path("experience/add/", views.create_experience, name="create_experience"),
    path(
        "experience/<uuid:experience_id>/edit/",
        views.update_experience,
        name="update_experience",
    ),
    path(
        "experience/<uuid:experience_id>/delete/",
        views.delete_experience,
        name="delete_experience",
    ),
    # Project
    path("projects/", views.projects, name="projects"),
    path("projects/add/", views.create_project, name="create_project"),
    path("projects/<slug:slug>/edit/", views.update_project, name="update_project"),
    path(
        "projects/<uuid:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    # API
    path("api/projects/", views.get_projects_json, name="get_projects_json"),
]
