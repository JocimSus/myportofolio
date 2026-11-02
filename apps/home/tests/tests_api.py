from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import Project


class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="api-user", password="secret")
        self.project = Project.objects.create(
            title="Portfolio Project",
            slug="portfolio-project",
            description="A project description.",
            category="website",
            technologies=["Django", "HTMX"],
            project_url="https://example.com",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])

    def grant(self, *codenames):
        permissions = Permission.objects.filter(
            content_type__app_label="home", codename__in=codenames
        )
        self.user.user_permissions.add(*permissions)
        for cache_name in ("_perm_cache", "_user_perm_cache", "_group_perm_cache"):
            self.user.__dict__.pop(cache_name, None)

    def test_anonymous_user_can_list_projects(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], self.project.title)
        self.assertEqual(response.json()[0]["star_count"], 0)

    def test_detail_returns_json_for_htmx_request(self):
        response = self.client.get(
            self.detail_url,
            HTTP_ACCEPT="application/json",
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["title"], self.project.title)

    def test_list_can_filter_by_title(self):
        response = self.client.get(self.list_url, {"title": "portfolio"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_requires_add_permission(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title": "<b>New Project</b>",
            "description": "Description",
            "category": "website",
            "technologies": "Django, HTMX",
        }

        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, 403)

        self.grant("add_project")
        response = self.client.post(self.list_url, payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["title"], "New Project")
        self.assertEqual(response.json()["technologies"], ["Django", "HTMX"])

    def test_update_requires_change_permission(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.detail_url, {"title": "Updated"})

        self.assertEqual(response.status_code, 403)

        self.grant("change_project")
        response = self.client.patch(self.detail_url, {"title": "<i>Updated</i>"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated")

    def test_delete_requires_delete_permission(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)

        self.grant("delete_project")
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_star_requires_authentication_and_toggles_state(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.user)
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_starred"])
        self.assertEqual(response.json()["star_count"], 1)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_starred"])
        self.assertEqual(response.json()["star_count"], 0)

    def test_detail_returns_404_for_unknown_project(self):
        url = reverse(
            "api:project-detail", args=["00000000-0000-0000-0000-000000000000"]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
