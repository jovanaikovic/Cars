# Generated by Django 4.2.5 on 2023-09-24 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
