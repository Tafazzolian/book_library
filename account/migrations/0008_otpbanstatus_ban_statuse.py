# Generated by Django 4.2.4 on 2023-09-04 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_otpbanstatus_otpcode_created2'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpbanstatus',
            name='ban_statuse',
            field=models.BooleanField(default=False),
        ),
    ]
