# Generated by Django 4.1.3 on 2023-01-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_brand_language_brand_languages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Niche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niche', models.CharField(blank=True, choices=[('Entertainment', 'Entertainment'), ('Hospitalities', 'Hospitalities'), ('Football', 'Football')], max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='brand',
            name='niche',
        ),
        migrations.RemoveField(
            model_name='influencer',
            name='niche',
        ),
        migrations.AddField(
            model_name='brand',
            name='niches',
            field=models.ManyToManyField(blank=True, max_length=200, to='users.niche'),
        ),
        migrations.AddField(
            model_name='influencer',
            name='niches',
            field=models.ManyToManyField(blank=True, max_length=200, to='users.niche'),
        ),
    ]
