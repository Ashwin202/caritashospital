# Generated by Django 3.2.22 on 2023-10-28 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caritasapp', '0022_alter_contact_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='department',
            field=models.ForeignKey(default='Rheumatology', null=True, on_delete=django.db.models.deletion.CASCADE, to='caritasapp.department'),
        ),
    ]
