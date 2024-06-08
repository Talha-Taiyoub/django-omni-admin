# Generated by Django 5.0.6 on 2024-06-08 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0012_amenities_roomcategory_gallery_roomamenities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomamenities',
            name='room_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_amenities_set', to='segment.roomcategory'),
        ),
    ]
