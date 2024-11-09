# Generated by Django 5.1 on 2024-11-09 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refuel', '0011_alter_gymmembership_additional_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='refuel/images')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_set', to='refuel.restaurant')),
            ],
        ),
        migrations.DeleteModel(
            name='Gallery',
        ),
    ]