from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_about_goal_mission_service_vission'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vission',
            new_name='Vision',
        ),
    ]
