from apps.home.models import Project

projects = [
    {
        "title": "Open House Fasilkom 2026",
        "slug": "open-house-fasilkom-2026",
        "description": "Main website for Open House Fasilkom's Event.",
        "thumbnail": "https://zip.jocimsus.tech/u/599400ab-9f4b-4ebb-9655-147987077d5b.webp",
        "project_url": "https://oh.cs.ui.ac.id",
        "technologies": [
            {
                "name": "React",
                "icon": "home/icons/react.svg",
            },
            {
                "name": "Hono",
                "icon": "home/icons/bun.svg",
            },
        ],
        "category": "website",
    },
    {
        "title": "COMPFEST 18",
        "slug": "compfest-18",
        "description": "Main website for COMPFEST 18's Event.",
        "thumbnail": "https://zip.jocimsus.tech/u/6fa7bd84-31a5-49df-8b8f-4469c860e979.webp",
        "project_url": "https://compfest.id",
        "technologies": [
            {
                "name": "Docker",
                "icon": "home/icons/docker.svg",
            },
            {
                "name": "GitHub Actions",
                "icon": "home/icons/github.svg",
            },
            {
                "name": "Next.js",
                "icon": "home/icons/next-js.svg",
            },
            {
                "name": "TanStack",
                "icon": "home/icons/tanstack.svg",
            },
        ],
        "category": "website",
    },
    {
        "title": "Portofolio",
        "slug": "portofolio",
        "description": "My personal portfolio website.",
        "thumbnail": "https://zip.jocimsus.tech/u/6f3994ac-6205-4c9b-9848-76b9625a817c.webp",
        "project_url": "https://joachim-susatiyo-portofolio.pws.cs.ui.ac.id",
        "technologies": [
            {
                "name": "Django",
                "icon": "home/icons/django.svg",
            },
            {
                "name": "TailwindCSS",
                "icon": "home/icons/tailwind-css.svg",
            },
        ],
        "category": "website",
    },
]


for project in projects:
    Project.objects.update_or_create(
        title=project["title"],
        slug=project["slug"],
        description=project["description"],
        thumbnail=project["thumbnail"],
        project_url=project["project_url"],
        technologies=project["technologies"],
        category=project["category"],
    )
