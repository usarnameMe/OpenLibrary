# Generated by Django 5.1.1 on 2024-12-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
