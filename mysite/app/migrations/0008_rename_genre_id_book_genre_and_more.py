# Generated by Django 4.2.6 on 2023-11-04 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_book_cover_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='owner_id',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='book',
            name='condition_desc',
            field=models.CharField(default='GOOD', max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(default='AVAILABLE', max_length=50),
        ),
    ]
