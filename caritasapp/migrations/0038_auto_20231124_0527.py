# Generated by Django 3.2.22 on 2023-11-24 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caritasapp', '0037_album_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sliderimage',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sliderimage',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
