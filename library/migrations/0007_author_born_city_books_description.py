# Generated by Django 4.2.4 on 2023-08-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_remove_author_featured_books_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='born_city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.TextField(null=True),
        ),
    ]