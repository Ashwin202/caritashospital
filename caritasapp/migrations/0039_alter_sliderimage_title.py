# Generated by Django 3.2.22 on 2023-11-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caritasapp', '0038_auto_20231124_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sliderimage',
            name='title',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
