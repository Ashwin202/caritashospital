# Generated by Django 3.2.22 on 2023-11-27 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caritasapp', '0041_mobilesliderimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilesliderimage',
            name='image',
            field=models.ImageField(upload_to='mobileslider_images/'),
        ),
    ]
