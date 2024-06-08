# Generated by Django 5.0.6 on 2024-06-08 16:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0011_branchstaff_delete_branchmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Out Of Order', 'Out Of order')], default='Out Of Order', max_length=15)),
                ('featured_image', models.ImageField(upload_to='segment/images')),
                ('overview', models.TextField()),
                ('panorama', models.ImageField(upload_to='segment/images')),
                ('adults', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('children', models.PositiveSmallIntegerField()),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount_in_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='segment.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='segment/images')),
                ('room_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='segment.roomcategory')),
            ],
        ),
        migrations.CreateModel(
            name='RoomAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='segment.amenities')),
                ('room_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='segment.roomcategory')),
            ],
            options={
                'unique_together': {('room_category', 'amenity')},
            },
        ),
    ]