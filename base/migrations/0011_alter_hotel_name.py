# Generated by Django 4.1.7 on 2023-03-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0010_remove_hotel_other_column"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hotel",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]