# Generated by Django 4.2.5 on 2023-10-01 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0012_vehicle_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('denied', 'denied')], default='pending', max_length=10),
        ),
    ]
