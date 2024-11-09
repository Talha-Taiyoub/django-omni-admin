# Generated by Django 5.1 on 2024-11-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0042_alter_cart_check_in_alter_cart_check_out'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='created_at',
        ),
        migrations.AddField(
            model_name='story',
            name='header',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='story',
            name='tag1',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='tag2',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='tag3',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
