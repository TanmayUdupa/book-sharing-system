# Generated by Django 4.2.6 on 2023-11-15 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_delete_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(default='Earth', max_length=100),
        ),
    ]
