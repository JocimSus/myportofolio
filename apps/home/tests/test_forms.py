from django.test import TestCase

from ..forms import ExperienceForm, ProjectForm
from ..models import Experience, Project


class ProjectFormTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "title": "Portfolio Website",
            "description": "Personal site built with Django",
            "thumbnail": "https://example.com/thumb.png",
            "project_url": "https://example.com",
            "technologies": "Django, React, Next.js",
            "category": "website",
        }

    # CREATE
    def test_create_form_valid_data(self):
        form = ProjectForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_create_form_saves_new_project(self):
        form = ProjectForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        project = form.save()

        self.assertIsInstance(project, Project)
        self.assertEqual(project.title, "Portfolio Website")
        self.assertEqual(project.technologies, ["Django", "React", "Next.js"])
        self.assertEqual(Project.objects.count(), 1)

    # FORMATTING
    def test_clean_technologies_parses_comma_separated_string(self):
        data = self.valid_form_data.copy()
        data["technologies"] = " Django , React , Next.js "
        form = ProjectForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["technologies"],
            ["Django", "React", "Next.js"],
        )

    def test_clean_technologies_empty_input(self):
        data = self.valid_form_data.copy()
        data["technologies"] = ""
        form = ProjectForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["technologies"], [])

    def test_form_invalid_when_required_fields_missing(self):
        data = self.valid_form_data.copy()
        data["title"] = ""
        form = ProjectForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    # UPDATE
    def test_update_form_initial_data_conversion(self):
        project = Project.objects.create(
            title="Old Project",
            description="Old description",
            technologies=["Django", "Docker", "TailwindCSS"],
            category="website",
        )
        form = ProjectForm(instance=project)
        self.assertEqual(form.initial["technologies"], "Django, Docker, TailwindCSS")

    def test_update_form_saves_updated_project(self):
        project = Project.objects.create(
            title="Old Title",
            description="Old Desc",
            technologies=["Django"],
            category="website",
        )

        update_data = {
            "title": "New Title",
            "description": "Updated Desc",
            "thumbnail": "https://example.com/new.png",
            "project_url": "https://example.com/new",
            "technologies": "Django, Vue, PostgreSQL",
            "category": "website",
        }

        form = ProjectForm(data=update_data, instance=project)
        self.assertTrue(form.is_valid())
        updated_project = form.save()

        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(updated_project.pk, project.pk)
        self.assertEqual(updated_project.title, "New Title")
        self.assertEqual(updated_project.technologies, ["Django", "Vue", "PostgreSQL"])


class ExperienceFormTest(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "title": "Site Reliability Engineer Intern",
            "description": "Maintained and improved the reliability of web applications.",
            "category": "internship",
            "thumbnail": "https://example.com/thumb.png",
            "start_date": "2026-06-01",
            "end_date": "2026-09-01",
        }

    # CREATE
    def test_create_experience_form_valid_data(self):
        form = ExperienceForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_create_experience_form_saves_new_experience(self):
        form = ExperienceForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        experience = form.save()

        self.assertIsInstance(experience, Experience)
        self.assertEqual(experience.title, "Site Reliability Engineer Intern")
        self.assertEqual(Experience.objects.count(), 1)

    # UPDATE
    def test_update_form_saves_updated_experience(self):
        experience = Experience.objects.create(
            title="Old",
            description="Old",
            category="internship",
            start_date="2026-01-01",
            end_date="2026-03-01",
        )

        update_data = {
            "title": "New",
            "description": "Updated",
            "category": "internship",
            "thumbnail": "https://example.com/new.png",
            "start_date": "2025-02-01",
            "end_date": "2025-04-01",
        }

        form = ExperienceForm(data=update_data, instance=experience)
        self.assertTrue(form.is_valid())
        updated_experience = form.save()

        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(updated_experience.pk, experience.pk)
        self.assertEqual(updated_experience.title, "New")
        self.assertEqual(updated_experience.description, "Updated")
        self.assertEqual(updated_experience.category, "internship")
        self.assertEqual(updated_experience.thumbnail, "https://example.com/new.png")
        self.assertEqual(updated_experience.start_date, "2025-02-01")
        self.assertEqual(updated_experience.end_date, "2025-04-01")

    # DELETE
    def test_delete_experience(self):
        experience = Experience.objects.create(
            title="Deleted",
            description="Deleted.",
            category="internship",
            start_date="2026-01-01",
            end_date="2026-03-01",
        )
        self.assertEqual(Experience.objects.count(), 1)
        experience.delete()
        self.assertEqual(Experience.objects.count(), 0)
