# Generated by Django 3.2.8 on 2023-06-20 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_auto_20230619_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='service',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)]),
        ),
    ]
