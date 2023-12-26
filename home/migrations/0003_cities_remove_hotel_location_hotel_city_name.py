# Generated by Django 5.0 on 2023-12-24 16:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_hotel_location_alter_hotel_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('city_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='location',
        ),
        migrations.AddField(
            model_name='hotel',
            name='city_name',
            field=models.ManyToManyField(to='home.cities'),
        ),
    ]
