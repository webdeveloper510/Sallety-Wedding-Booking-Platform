# Generated by Django 4.2 on 2025-04-28 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_booking_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.venue'),
        ),
    ]
