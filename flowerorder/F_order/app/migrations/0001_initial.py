# Generated by Django 5.1.3 on 2024-12-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='flowerorde/png')),
                ('name', models.CharField(max_length=100)),
                ('price', models.ImageField(upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
