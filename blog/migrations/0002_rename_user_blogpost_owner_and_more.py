# Generated by Django 4.1.3 on 2023-01-07 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='user',
            new_name='owner',
        ),
    ]