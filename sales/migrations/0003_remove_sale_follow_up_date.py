# Generated by Django 5.1.4 on 2025-03-19 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_sale_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='follow_up_date',
        ),
    ]
