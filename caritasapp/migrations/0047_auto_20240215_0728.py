# Generated by Django 3.2.23 on 2024-02-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caritasapp', '0046_auto_20240131_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='order',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='videos',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='studies',
            name='investigators',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='videos',
            name='title',
            field=models.CharField(max_length=1000),
        ),
    ]
