# Generated by Django 5.0 on 2023-12-24 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_hotel_city_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='city_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='home.cities'),
        ),
    ]
