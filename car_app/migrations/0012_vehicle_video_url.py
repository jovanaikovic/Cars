# Generated by Django 4.2.5 on 2023-10-01 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0011_vehicle_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='video_url',
            field=models.URLField(null=True),
        ),
    ]
