from django.db import migrations


def create_roles_teams(apps, schema_editor):
    roles = {
        "developer": "the person on the team who does the work",
        "scrum master": "the team's coach",
        "product owner": "the person who defines the work"
    }
    Role = apps.get_model("accounts", "Role")
    for name, description in roles.items():
        role_obj = Role(name=name, description=description)
        role_obj.save()
    
    teams = {
        "alpha": "the A team",
        "bravo": "the B team",
        "charlie": "the C team"
    }
    Team = apps.get_model("accounts", "Team")
    for name, description in teams.items():
        team_obj = Team(name=name, description=description)
        team_obj.save()



class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles_teams),

    ]
