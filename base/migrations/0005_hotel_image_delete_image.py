# Generated by Django 4.1.7 on 2023-03-20 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0004_image_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="hotel",
            name="image",
            field=models.ImageField(null=True, upload_to="images"),
        ),
        migrations.DeleteModel(
            name="Image",
        ),
    ]
