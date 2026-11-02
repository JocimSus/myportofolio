from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Experience, Project


def grant_editor_permissions(group):
    group.permissions.add(
        Permission.objects.get(codename="change_project"),
        Permission.objects.get(codename="change_experience"),
    )


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
        self.assertContains(response, f'href="{reverse("home:profile")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, "No experiences added yet.")


class ProjectViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="My Project",
            slug="my-project",
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
        self.assertContains(
            response,
            f'href="{reverse("home:project_detail", args=[self.project.slug])}"',
        )

    def test_project_create_modal_uses_htmx_json_api(self):
        user = User.objects.create_user(username="project-owner", password="secret")
        user.user_permissions.add(Permission.objects.get(codename="add_project"))
        self.client.force_login(user)

        response = self.client.get(reverse("home:projects"))

        self.assertContains(response, 'hx-post="/api/v1/projects/"')
        self.assertContains(response, '"Accept": "application/json"')

    def test_project_delete_uses_confirmation_modal(self):
        user = User.objects.create_user(username="project-editor", password="secret")
        user.user_permissions.add(Permission.objects.get(codename="delete_project"))
        self.client.force_login(user)

        response = self.client.get(reverse("home:projects"))

        self.assertContains(response, 'id="delete-project-modal"')
        self.assertContains(response, 'class="delete-project-trigger')
        self.assertContains(response, f'data-project-id="{self.project.id}"')
        self.assertNotContains(response, "hx-confirm=")

    def test_empty_project_page(self):
        Project.objects.all().delete()

        response = self.client.get(reverse("home:projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No projects added yet.")

    def test_project_detail_page(self):
        response = self.client.get(
            reverse("home:project_detail", args=[self.project.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/project_detail.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Django")
        self.assertContains(response, "React")
        self.assertContains(response, "https://cdn.simpleicons.org/django")
        self.assertContains(response, "https://cdn.simpleicons.org/react")
        self.assertContains(response, self.project.project_url)

    def test_project_detail_page_not_found(self):
        response = self.client.get(
            reverse("home:project_detail", args=["does-not-exist"])
        )

        self.assertEqual(response.status_code, 404)


class ProjectFormViewTest(TestCase):
    def setUp(self):
        self.editor_group = Group.objects.create(name="editor")
        grant_editor_permissions(self.editor_group)

        self.superuser = User.objects.create_superuser(
            username="superuser", email="superuser@mail.com", password="password123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="password123"
        )
        self.editor.groups.add(self.editor_group)

        self.project = Project.objects.create(
            title="My Project",
            slug="my-project",
            description="Sample project.",
            category="website",
            technologies=["Django", "React"],
            project_url="https://github.com",
        )

    def test_project_form_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("home:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/project_form.html")
        self.assertContains(response, "Add New Projects")
        self.assertContains(response, f'href="{reverse("home:projects")}"')

    def test_project_form_submission(self):
        self.client.force_login(self.superuser)
        form_data = {
            "title": "New Project",
            "description": "New project.",
            "category": "website",
            "technologies": "Django, React",
            "project_url": "https://example.com",
            "thumbnail": "https://example.com/thumbnail.png",
        }
        response = self.client.post(reverse("home:create_project"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)

    def test_update_project_form_view(self):
        self.client.force_login(self.editor)
        response = self.client.get(
            reverse("home:update_project", args=[self.project.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/project_form.html")
        self.assertContains(response, self.project.title)

    def test_update_project_form_submission(self):
        self.client.force_login(self.editor)
        update_data = {
            "title": "Updated Project",
            "description": "Updated project.",
            "category": "website",
            "technologies": "Django, Vue",
            "project_url": "https://example.com",
        }
        response = self.client.post(
            reverse("home:update_project", args=[self.project.slug]),
            data=update_data,
        )

        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Project")

    def test_delete_project_submission(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("home:delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 0)


class ExperienceFormViewTest(TestCase):
    def setUp(self):
        self.editor_group = Group.objects.create(name="editor")
        grant_editor_permissions(self.editor_group)

        self.superuser = User.objects.create_superuser(
            username="superuser", email="superuser@mail.com", password="password123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="password123"
        )
        self.editor.groups.add(self.editor_group)

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            start_date="2026-01-01",
        )

    def test_create_experience_form_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("home:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/experience_form.html")
        self.assertContains(response, f'href="{reverse("home:experience")}"')

    def test_create_experience_form_submission(self):
        self.client.force_login(self.superuser)
        form_data = {
            "title": "Software Engineer Intern",
            "description": "Mengembangkan aplikasi web.",
            "category": "internship",
            "start_date": "2026-06-01",
            "end_date": "2026-09-01",
        }
        response = self.client.post(reverse("home:create_experience"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 2)

    def test_update_experience_form_view(self):
        self.client.force_login(self.editor)
        response = self.client.get(
            reverse("home:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/experience_form.html")
        self.assertContains(response, self.experience.title)

    def test_update_experience_form_submission(self):
        self.client.force_login(self.editor)
        update_data = {
            "title": "Asisten Dosen PBP Updated",
            "description": "Membantu mahasiswa memahami Django.",
            "category": "part-time",
            "start_date": "2026-01-01",
        }
        response = self.client.post(
            reverse("home:update_experience", args=[self.experience.id]),
            data=update_data,
        )

        self.assertEqual(response.status_code, 302)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP Updated")

    def test_delete_experience_submission(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("home:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Experience.objects.count(), 0)


class RoleAuthorizationTest(TestCase):
    def setUp(self):
        self.editor_group = Group.objects.create(name="editor")
        grant_editor_permissions(self.editor_group)

        self.regular_user = User.objects.create_user(
            username="regular_user", password="password123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="password123"
        )
        self.editor.groups.add(self.editor_group)
        self.superuser = User.objects.create_superuser(
            username="superuser", email="superuser@mail.com", password="password123"
        )

        self.project = Project.objects.create(
            title="Sample Project",
            slug="sample-project",
            description="Sample project.",
            category="website",
        )
        self.experience = Experience.objects.create(
            title="Sample Experience",
            description="Sample experience.",
            category="part-time",
            start_date="2026-01-01",
        )

    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse("home:create_project"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

        response = self.client.get(
            reverse("home:update_project", args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_regular_user_forbidden_on_restricted_actions(self):
        self.client.force_login(self.regular_user)

        response = self.client.get(reverse("home:create_project"))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(
            reverse("home:update_project", args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            reverse("home:delete_project", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        response = self.client.get(
            reverse("home:update_project", args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("home:create_project"))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(
            reverse("home:delete_project", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_superuser_has_full_access(self):
        self.client.force_login(self.superuser)

        response = self.client.get(reverse("home:create_project"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse("home:update_project", args=[self.project.slug])
        )
        self.assertEqual(response.status_code, 200)


class StarTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.project = Project.objects.create(
            title="Star Project",
            slug="star-project",
            description="Project untuk tes star.",
            category="website",
        )

    def test_toggle_star_add_and_remove(self):
        self.client.force_login(self.user1)
        url = reverse("home:toggle_star", args=[self.project.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project.starred_by.count(), 1)
        self.assertIn(self.user1, self.project.starred_by.all())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_multiple_users_starring_same_project(self):
        url = reverse("home:toggle_star", args=[self.project.id])

        self.client.force_login(self.user1)
        self.client.post(url)

        self.client.force_login(self.user2)
        self.client.post(url)

        self.assertEqual(self.project.starred_by.count(), 2)


class HtmxProjectViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="password123"
        )
        self.project = Project.objects.create(
            title="Portfolio Project",
            slug="portfolio-project",
            description="Project rendered by HTMX.",
            category="website",
            technologies=["Django"],
            thumbnail="https://example.com/project.png",
            project_url="https://example.com/project",
        )
        self.headers = {"HTTP_HX_REQUEST": "true"}

    def test_search_returns_project_cards_fragment(self):
        response = self.client.get(
            reverse("home:projects"), {"title": "Portfolio"}, **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertNotContains(response, "<html", html=False)

    def test_create_project_returns_cards_for_htmx_and_json_for_regular_ajax(self):
        self.client.force_login(self.superuser)
        form_data = {
            "title": "HTMX Project",
            "description": "Created without a full reload.",
            "category": "website",
            "technologies": "Django, HTMX",
            "thumbnail": "https://example.com/htmx.png",
            "project_url": "https://example.com/htmx",
        }

        response = self.client.post(
            reverse("home:create_project_ajax"), form_data, **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HTMX Project")
        self.assertEqual(Project.objects.filter(title="HTMX Project").count(), 1)

        form_data["title"] = "JSON Project"
        response = self.client.post(reverse("home:create_project_ajax"), form_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_invalid_project_retargets_form_fields(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse("home:create_project_ajax"), {"title": ""}, **self.headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Retarget"], "#project-form-fields")

    def test_delete_project_accepts_htmx_delete(self):
        self.client.force_login(self.superuser)

        response = self.client.delete(
            reverse("home:delete_project_ajax", args=[self.project.id]),
            data="title=Portfolio",
            content_type="application/x-www-form-urlencoded",
            **self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertContains(response, "No projects added yet or found.")


class HtmxExperienceViewTest(TestCase):
    def setUp(self):
        editor_group = Group.objects.create(name="editor")
        grant_editor_permissions(editor_group)
        self.superuser = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="password123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="password123"
        )
        self.editor.groups.add(editor_group)
        self.experience = Experience.objects.create(
            title="Teaching Assistant",
            description="Supporting students in class.",
            category="part-time",
            start_date="2026-01-01",
            thumbnail="https://example.com/experience.png",
        )
        self.headers = {"HTTP_HX_REQUEST": "true"}

    def test_experience_page_is_server_rendered(self):
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)

    def test_experience_page_uses_delete_modal_and_preserves_invalid_form_modal(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, 'id="delete-experience-modal"')
        self.assertContains(response, 'class="delete-experience-trigger')
        self.assertContains(response, f'data-experience-id="{self.experience.id}"')
        self.assertNotContains(response, "hx-confirm=")
        self.assertContains(
            response,
            'elt?.id !== "experience-form"',
        )
        self.assertNotContains(response, "hx-on::after-request")

    def test_experience_forms_use_post_and_explicit_csrf_headers(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("home:experience"))

        self.assertContains(response, 'hx-post="/experience/add-ajax/"')
        self.assertContains(response, 'hx-headers=\'{"X-CSRFToken": "')
        self.assertNotContains(response, "hx-put=")

        response = self.client.get(
            reverse("home:experience_edit_fragment", args=[self.experience.id]),
            **self.headers,
        )

        self.assertContains(
            response,
            f'hx-post="/experience/{self.experience.id}/edit/ajax/"',
        )
        self.assertContains(response, self.experience.title)

    def test_form_fragments_follow_permissions(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse("home:experience_form_fragment"), **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "experience-form")

        self.client.force_login(self.editor)
        response = self.client.get(
            reverse("home:experience_edit_fragment", args=[self.experience.id]),
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.title)

    def test_create_and_update_experience_with_htmx(self):
        self.client.force_login(self.superuser)
        create_data = {
            "title": "HTMX Internship",
            "description": "Created without a full reload.",
            "category": "internship",
            "thumbnail": "https://example.com/internship.png",
            "start_date": "2026-06-01",
            "end_date": "2026-09-01",
        }
        response = self.client.post(
            reverse("home:create_experience_ajax"), create_data, **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HTMX Internship")
        self.assertNotContains(response, "hx-swap-oob")

        self.client.force_login(self.editor)
        response = self.client.post(
            reverse("home:update_experience_ajax", args=[self.experience.id]),
            data={
                "title": "Updated Assistant",
                "description": "Updated using HTMX.",
                "category": "part-time",
                "thumbnail": "https://example.com/experience.png",
                "start_date": "2026-01-01",
                "end_date": "",
            },
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Assistant")

    def test_invalid_experience_retargets_form_and_delete_accepts_htmx(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("home:create_experience_ajax"), {"title": ""}, **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Retarget"], "#experience-form-container")

        response = self.client.delete(
            reverse("home:delete_experience_ajax", args=[self.experience.id]),
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertContains(response, "No experiences added yet.")


class ApiEndpointIntegrityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="secretpassword"
        )
        self.project = Project.objects.create(
            title="API Project",
            slug="api-project",
            description="Testing API JSON.",
            category="website",
        )
        self.project.starred_by.add(self.user)

    def test_get_projects_json_does_not_leak_sensitive_info(self):
        url = reverse("home:get_projects_json")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        content = response.content.decode("utf-8")
        self.assertNotIn("pbkdf2_sha256", content)
        self.assertNotIn("secretpassword", content)
