from django.test import TestCase

from ..forms import ProjectForm
from ..models import Project


class ProjectFormTest(TestCase):
    def test_project_form_valid_data(self):
        form_data = {
            "title": "Test Project",
            "description": "Test Description",
            "thumbnail": "https://example.com/image.png",
            "project_url": "https://example.com",
            "technologies": "Django, React, Next.js",
            "category": "website",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_technologies_parses_comma_separated_string(self):
        form_data = {
            "title": "Test Project",
            "description": "Test Description",
            "technologies": " Django , React , Next.js ",
            "category": "website",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["technologies"],
            ["Django", "React", "Next.js"],
        )

    def test_clean_technologies_empty_input(self):
        form_data = {
            "title": "Test Project",
            "description": "Test Description",
            "technologies": "",
            "category": "website",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["technologies"], [])

    def test_form_initial_technologies_conversion_on_edit(self):
        project = Project.objects.create(
            title="Existing Project",
            description="Desc",
            technologies=["Django", "React"],
            category="website",
        )
        form = ProjectForm(instance=project)
        self.assertEqual(form.initial["technologies"], "Django, React")
