# Generated by Django 4.1.7 on 2023-03-31 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_category_city_country_guest_reservation_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ReservationStatusEvents",
            new_name="ReservationStatusEvent",
        ),
        migrations.RenameModel(
            old_name="RoomReserved",
            new_name="ReservedRoom",
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="city",
            options={"verbose_name_plural": "Cities"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"verbose_name_plural": "Countries"},
        ),
    ]
