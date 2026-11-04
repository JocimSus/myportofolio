from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Experience, Project
from .permissions import (
    IsExperienceOwnerOrEditorOrReadOnly,
    IsProjectOwnerOrEditorOrReadOnly,
)
from .serializers import ExperienceSerializer, ProjectSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsProjectOwnerOrEditorOrReadOnly])
def project_list(request):
    projects = Project.objects.prefetch_related("starred_by").order_by("title")
    title = request.query_params.get("title", "").strip()
    if title:
        projects = projects.filter(title__icontains=title)

    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsProjectOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id
    )

    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    relation = project.starred_by.filter(pk=request.user.pk)
    if relation.exists():
        relation.delete()
    else:
        project.starred_by.add(request.user)

    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsExperienceOwnerOrEditorOrReadOnly])
def experience_list(request):
    experiences = Experience.objects.order_by("start_date")
    title = request.query_params.get("title", "").strip()
    if title:
        experiences = experiences.filter(title__icontains=title)

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsExperienceOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
