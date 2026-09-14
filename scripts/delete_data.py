from apps.home.models import Experience, Project

Experience.objects.all().delete()
Project.objects.all().delete()
