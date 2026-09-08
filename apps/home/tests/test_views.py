from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Experience, Project


class HomeViewTest(TestCase):
    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)


class ProfileViewTest(TestCase):
    def test_profile_url_is_accessible(self):
        response = self.client.get(reverse("home:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/profile.html")
        self.assertContains(response, "profile")
        self.assertContains(response, f'href="{reverse("home:experience")}"')

    def test_profile_page(self):
        response = self.client.get(reverse("home:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/profile.html")
        self.assertContains(response, "Joachim Susatiyo")
        self.assertContains(response, "Ilmu Komputer - S1")
        self.assertContains(
            response, "a passionate computer science student at Universitas Indonesia."
        )
        self.assertContains(response, f'href="{reverse("home:experience")}"')


class ExperienceViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            start_date=timezone.now(),
        )

    def test_experience_url_is_accessible(self):
        response = self.client.get(reverse("home:experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/experience.html")
        self.assertContains(response, f'href="{reverse("home:experience")}"')

    def test_experience_page(self):
        response = self.client.get(reverse("home:experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("home:profile")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, "No experiences added yet.")

    def test_completed_experience_rendering(self):
        self.experience.end_date = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class ProjectViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="My Project",
            description="Sample project.",
            category="website",
            technologies=["Django", "React"],
            project_url="https://github.com",
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("home:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/projects.html")
        self.assertContains(response, f'href="{reverse("home:profile")}"')

    def test_project_page(self):
        response = self.client.get(reverse("home:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/projects.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Website")
        self.assertContains(response, f'href="{reverse("home:profile")}"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("home:projects"))

        self.assertContains(response, "No projects added yet.")
