# Generated by Django 4.2.4 on 2023-08-17 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_otpcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpcode',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
