# Generated by Django 4.2.6 on 2023-11-04 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_book_cover_image_alter_book_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='location',
        ),
    ]