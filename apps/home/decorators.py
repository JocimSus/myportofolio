from functools import wraps

from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = set(request.user.groups.values_list("name", flat=True))
            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return _wrapped_view

    return decorator


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
