# Generated by Django 4.2.5 on 2023-10-06 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0015_vehiclegallery'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiclegallery',
            old_name='image1',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image4',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image5',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image6',
        ),
        migrations.RemoveField(
            model_name='vehiclegallery',
            name='image7',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='car_body',
            field=models.CharField(choices=[('Limuzina', 'Limuzina'), ('SUV', 'SUV'), ('Karavan', 'Karavan'), ('Kupe', 'Kupe'), ('Kabriolet', 'Kabriolet')], default='Limuuzina', max_length=15),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(choices=[('Benzin', 'Benzin'), ('Dizel', 'Dizel'), ('Električno', 'Električno'), ('Hibrid', 'Hibrid')], max_length=100),
        ),
        migrations.AlterField(
            model_name='vehiclegallery',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='car_app.vehicle'),
        ),
    ]
