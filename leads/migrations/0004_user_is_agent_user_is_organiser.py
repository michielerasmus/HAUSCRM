# Generated by Django 5.1.4 on 2025-03-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_userprofile_agent_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=True),
        ),
    ]
