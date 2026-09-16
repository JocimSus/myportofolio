from typing import ClassVar

from django.forms import ModelForm, Textarea, TextInput, URLInput

from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields: ClassVar[list] = [
            "title",
            "description",
            "thumbnail",
            "project_url",
            "technologies",
            "category",
        ]

        labels: ClassVar[dict] = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "thumbnail": "Thumbnail Proyek",
            "project_url": "URL Proyek",
            "technologies": "Teknologi yang Digunakan",
            "category": "Kategori Proyek",
        }

        widgets: ClassVar[dict] = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "technologies": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "website",
                }
            ),
        }
