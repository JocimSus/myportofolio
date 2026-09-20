from datetime import date

from apps.home.models import Experience

experiences = [
    {
        "title": "RISTEK",
        "description": "Member of RISTEK's Web Development SIG",
        "category": "organization",
        "thumbnail": "https://zip.jocimsus.tech/u/13ab0ace-04e9-4c67-b738-1b545eab1306.webp",
        "start_date": date(2026, 5, 1),
        "end_date": None,
    },
    {
        "title": "Open House Fasilkom 2026",
        "description": "Tech Lead for Open House Fasilkom 2026's website as Vice PIC of IT Development.",
        "category": "committee",
        "thumbnail": "https://zip.jocimsus.tech/u/7db40dd5-c57d-43e9-8e97-94f3cce37990.webp",
        "start_date": date(2026, 5, 1),
        "end_date": None,
    },
    {
        "title": "RISTEK Hackathon 2026",
        "description": "Winner of RISTEK Hackathon 2026.",
        "category": "competition",
        "thumbnail": "https://zip.jocimsus.tech/u/13ab0ace-04e9-4c67-b738-1b545eab1306.webp",
        "start_date": date(2026, 8, 10),
        "end_date": date(2026, 8, 15),
    },
]


for experience in experiences:
    Experience.objects.update_or_create(
        title=experience["title"],
        description=experience["description"],
        category=experience["category"],
        thumbnail=experience["thumbnail"],
        start_date=experience["start_date"],
        end_date=experience["end_date"],
    )
