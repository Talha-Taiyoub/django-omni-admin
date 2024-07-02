# Generated by Django 5.0.6 on 2024-07-02 15:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refuel', '0008_alter_gymgender_gender_alter_gymgender_gym'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='discount_in_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
