from django.db import migrations

def create_status(apps, schema_editor):
    status_entries={
        "to do":"an issue for which work has not yet started",
        "in progress":"an issue actively being worked on",
        "done":"an issue for which work has completed",
    }
    Status = apps.get_model("issues", "Status")
    for name,description in status_entries.items():
        status_obj=Status(name=name, description=description)
        status_obj.save()





class Migration(migrations.Migration):
    dependencies = [
        ('issues', '0002_alter_status_options'),
    ]

    operations = [
        migrations.RunPython(create_status),
    ]