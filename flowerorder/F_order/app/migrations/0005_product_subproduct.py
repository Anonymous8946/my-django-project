# Generated by Django 5.1.3 on 2024-12-04 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_subproduct'),
    ]

    operations = [
        migrations.AddField(
    model_name='product',
    name='subproduct',
    field=models.ForeignKey(
        to='app.SubProduct',
        on_delete=models.CASCADE,
        default=1  # Replace 1 with a valid `SubProduct` ID.
    ),
)
    ]
