from django.http import HttpRequest

from .selectors import get_default_context


def default_context_processor(_request: HttpRequest) -> dict:
    return get_default_context()
