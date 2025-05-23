# Generated by Django 5.1.4 on 2025-03-20 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rental',
            old_name='commission_percentage',
            new_name='management_commission_percentage',
        ),
        migrations.AddField(
            model_name='rental',
            name='placement_commission_percentage',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]
