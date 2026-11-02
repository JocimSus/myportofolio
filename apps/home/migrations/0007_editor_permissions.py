from django.db import migrations


def grant_editor_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    group = Group.objects.filter(name="editor").first()
    if group is None:
        return

    permissions = Permission.objects.filter(
        content_type__app_label="home",
        content_type__model__in=["project", "experience"],
        codename__in=["change_project", "change_experience"],
    )
    group.permissions.add(*permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_project_starred_by"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(grant_editor_permissions, migrations.RunPython.noop)
    ]
