# Generated by Django 5.0.6 on 2024-06-13 04:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0023_billing'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='placed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
