from functools import wraps

from django.conf import settings
from django.http import JsonResponse


def require_password(func):
    @wraps(func)
    def _wrapped_view(req, *args, **kwargs):
        if req.method == "POST":
            password = req.POST.get("password", "")

            if not password:
                return JsonResponse({"error": "Missing password"}, status=400)

            if password != settings.PASSWORD:
                return JsonResponse({"error": "Unauthorized"}, status=401)

        return func(req, *args, **kwargs)

    return _wrapped_view
