from django.test import TestCase
from django.utils import timezone

from ..models import Experience, Project


class ExperienceModelTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            start_date=timezone.now(),
        )

    def test_experience_str(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")

    def test_experience_category(self):
        self.assertEqual(self.experience.category, "part-time")

    def test_is_ongoing_property(self):
        self.assertTrue(self.experience.is_ongoing)

        self.experience.end_date = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="My Project",
            description="Sample project.",
            category="website",
            technologies=["Django", "React"],
            project_url="https://github.com",
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "My Project")

    def test_project_category(self):
        self.assertEqual(self.project.category, "website")

    def test_project_technologies(self):
        self.assertEqual(self.project.technologies, ["Django", "React"])

    def test_project_url(self):
        self.assertEqual(self.project.project_url, "https://github.com")
