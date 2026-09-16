from django.http import HttpRequest

from .selectors import get_default_context


def default(_request: HttpRequest) -> dict:
    return get_default_context()
