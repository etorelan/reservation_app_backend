# Generated by Django 4.1.7 on 2023-04-04 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0026_hoteldescription_hotel_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hotel",
            name="country",
        ),
    ]
