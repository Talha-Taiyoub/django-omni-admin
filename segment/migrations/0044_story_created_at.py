# Generated by Django 5.1 on 2024-11-09 13:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0043_remove_story_created_at_story_header_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
