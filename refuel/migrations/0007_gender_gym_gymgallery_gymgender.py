# Generated by Django 5.0.6 on 2024-07-02 14:36

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refuel', '0006_alter_reservation_total_bill'),
        ('segment', '0033_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Out Of Order', 'Out Of order')], default='Active', max_length=15)),
                ('featured_image', models.ImageField(upload_to='refuel/images')),
                ('overview', models.TextField()),
                ('area', models.PositiveSmallIntegerField()),
                ('fees', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('opening', models.TimeField()),
                ('closing', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='segment.branch')),
            ],
        ),
        migrations.CreateModel(
            name='GymGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='refuel/images')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='refuel.gym')),
            ],
        ),
        migrations.CreateModel(
            name='GymGender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gender_allowance', to='refuel.gender')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='refuel.gym')),
            ],
            options={
                'unique_together': {('gender', 'gym')},
            },
        ),
    ]
