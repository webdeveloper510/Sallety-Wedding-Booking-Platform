# Generated by Django 3.2.12 on 2025-04-29 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_remove_visitrequest_venue_id_visitrequest_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
