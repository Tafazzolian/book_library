# Generated by Django 4.2.4 on 2023-08-17 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_first_name_customuser_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
