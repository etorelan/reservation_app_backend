# Generated by Django 4.1.7 on 2023-03-31 21:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_alter_hotel_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "name",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Guest",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=30)),
                ("street_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="city_guests",
                        to="base.city",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="country_guests",
                        to="base.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
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
                ("check_in_date_time", models.DateTimeField()),
                ("check_out_date_time", models.DateTimeField()),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                ("time_modified", models.DateTimeField(auto_now=True)),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guest_reservations",
                        to="base.guest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReservationStatusCatalog",
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
                (
                    "status_name",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MaxValueValidator(4)]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Room",
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
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField()),
                (
                    "current_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RoomType",
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
                ("room_type", models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="location",
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="price_per_person",
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="service",
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="stars",
        ),
        migrations.AddField(
            model_name="hotel",
            name="review_count",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="review_rating",
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="star_rating",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="hotel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotel_images",
                to="base.hotel",
            ),
        ),
        migrations.CreateModel(
            name="RoomReserved",
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
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "reservation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservation_rooms",
                        to="base.reservation",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_room_reserved",
                        to="base.room",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="room",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hotel_rooms",
                to="base.hotel",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="room_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room_type_rooms",
                to="base.roomtype",
            ),
        ),
        migrations.CreateModel(
            name="ReservationStatusEvents",
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
                ("details", models.TextField()),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                (
                    "reservation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservation_status_events",
                        to="base.reservation",
                    ),
                ),
                (
                    "reservation_status_catalog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservation_catalog_status",
                        to="base.reservationstatuscatalog",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceGuest",
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
                ("time_issued", models.DateTimeField(auto_now_add=True)),
                ("time_paid", models.DateTimeField()),
                ("time_canceled", models.DateTimeField()),
                (
                    "invoice_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guest_invoices",
                        to="base.guest",
                    ),
                ),
                (
                    "reservation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservation_invoices",
                        to="base.reservation",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="country_cities",
                to="base.country",
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="category",
            field=models.ForeignKey(
                db_column="category_name",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category_hotels",
                to="base.category",
            ),
        ),
        migrations.AddField(
            model_name="hotel",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="city_hotels",
                to="base.city",
            ),
        ),
    ]
