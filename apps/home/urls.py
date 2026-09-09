from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("experience/", views.experience, name="experience"),
    path("projects/", views.projects, name="projects"),
]
