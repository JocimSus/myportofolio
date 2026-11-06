from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissionsOrAnonReadOnly,
)

from .models import Experience, Project


class IsPortfolioOwnerOrEditorOrReadOnly(DjangoModelPermissionsOrAnonReadOnly):
    model = None
    message = "You do not have permission to modify this resource."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if self.model is None:
            return False
        permissions = self.get_required_permissions(request.method, self.model)
        return request.user.has_perms(permissions)


class IsProjectOwnerOrEditorOrReadOnly(IsPortfolioOwnerOrEditorOrReadOnly):
    model = Project
    message = "You do not have permission to modify projects."


class IsExperienceOwnerOrEditorOrReadOnly(IsPortfolioOwnerOrEditorOrReadOnly):
    model = Experience
    message = "You do not have permission to modify experiences."
