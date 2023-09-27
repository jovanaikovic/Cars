# Generated by Django 4.2.5 on 2023-09-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0007_vehicle_image_vehicle_seat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='seat_number',
            field=models.IntegerField(choices=[('2', '2'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('11', '11')], default=5),
        ),
    ]