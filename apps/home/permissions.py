from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissionsOrAnonReadOnly,
)

from .models import Project


class IsPortfolioOwnerOrReadOnly(DjangoModelPermissionsOrAnonReadOnly):
    message = "You do not have permission to modify projects."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        permissions = self.get_required_permissions(request.method, Project)
        return request.user.has_perms(permissions)
