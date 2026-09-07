from django.db import models


class ExperienceType(models.TextChoices):
    INTERNSHIP = "internship", "Internship"
    RESEARCH = "research", "Research"
    VOLUNTEER = "volunteer", "Volunteer"
    PART_TIME = "part-time", "Part-Time"
    FULL_TIME = "full-time", "Full-Time"
    FREELANCE = "freelance", "Freelance"
    COMPETITION = "competition", "Competition"
    ORGANIZATION = "organization", "Organization"
    COMMITTEE = "committee", "Committee"
    COMMUNITY = "community", "Community"
