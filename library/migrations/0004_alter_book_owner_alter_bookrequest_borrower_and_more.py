# Generated by Django 5.1.1 on 2024-12-20 15:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_bookrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library_owned_books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookrequest',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library_borrowed_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookrequest',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='library_owned_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
