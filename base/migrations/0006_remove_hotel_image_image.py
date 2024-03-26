# Generated by Django 4.1.7 on 2023-03-20 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_hotel_image_delete_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hotel",
            name="image",
        ),
        migrations.CreateModel(
            name="Image",
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
                ("image", models.ImageField(null=True, upload_to="images")),
                (
                    "hotel",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="base.hotel",
                    ),
                ),
            ],
        ),
    ]
