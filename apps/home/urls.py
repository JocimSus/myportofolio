from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("experience/", views.experience, name="experience"),
    path("projects/", views.projects, name="projects"),
    path("projects/add/", views.create_project, name="create_project"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path(
        "projects/<uuid:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    path("api/projects/", views.get_projects_json, name="get_projects_json"),
]
