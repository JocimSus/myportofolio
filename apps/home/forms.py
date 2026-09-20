from typing import ClassVar

from django import forms
from django.forms import ModelForm, Textarea, TextInput, URLInput

from .models import Project


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.instance
            and self.instance.pk
            and isinstance(self.instance.technologies, list)
        ):
            self.initial["technologies"] = ", ".join(self.instance.technologies)

    def clean_technologies(self) -> list[str]:
        data = self.cleaned_data.get("technologies", "")
        if isinstance(data, str):
            return [tech.strip() for tech in data.split(",") if tech.strip()]
        return data

    technologies = forms.CharField(
        required=False,
        widget=TextInput(
            attrs={
                "placeholder": "Django, React, Next.js",
            }
        ),
        label="Teknologi yang Digunakan",
        help_text="Masukkan nama teknologi dipisah koma",
    )

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
            "category": TextInput(
                attrs={
                    "placeholder": "website",
                }
            ),
        }
