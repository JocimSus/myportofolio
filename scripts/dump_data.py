import json

from django.core import serializers

from apps.home.models import Experience, Project

print(
    json.dumps(
        {
            "experiences": json.loads(
                serializers.serialize("json", Experience.objects.all())
            ),
            "projects": json.loads(
                serializers.serialize("json", Project.objects.all())
            ),
        }
    )
)
