# Generated by Django 5.1 on 2024-11-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0044_story_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='author',
            field=models.CharField(default='Omni Residency', max_length=100),
        ),
    ]
