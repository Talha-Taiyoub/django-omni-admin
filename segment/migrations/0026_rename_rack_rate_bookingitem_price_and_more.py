# Generated by Django 5.0.6 on 2024-06-13 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('segment', '0025_alter_billing_discount_alter_billing_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingitem',
            old_name='rack_rate',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='bookingitem',
            name='discount_in_percentage',
        ),
    ]
