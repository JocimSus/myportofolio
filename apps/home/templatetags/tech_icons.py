from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def tech_icon_url(tech_name: str) -> str:
    tech_name_fmt = tech_name.replace(".", "dot")
    slug = slugify(tech_name_fmt)

    return f"https://cdn.simpleicons.org/{slug}"
