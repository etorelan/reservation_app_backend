# Generated by Django 4.1.7 on 2023-03-18 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hotel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("location", models.CharField(max_length=200)),
                ("pricePerPerson", models.FloatField()),
                ("service", models.PositiveSmallIntegerField()),
                ("stars", models.PositiveSmallIntegerField()),
                ("description", models.TextField()),
            ],
        ),
    ]
