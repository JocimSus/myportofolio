from django.test import TestCase
from django.utils import timezone

from ..models import Experience


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
