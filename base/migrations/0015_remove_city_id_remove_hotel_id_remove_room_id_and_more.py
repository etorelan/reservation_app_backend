# Generated by Django 4.1.7 on 2023-03-31 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0014_remove_country_id_alter_country_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="city",
            name="id",
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="id",
        ),
        migrations.RemoveField(
            model_name="room",
            name="id",
        ),
        migrations.RemoveField(
            model_name="roomtype",
            name="id",
        ),
        migrations.AlterField(
            model_name="city",
            name="name",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="hotel",
            name="name",
            field=models.CharField(
                max_length=100, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="name",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="roomtype",
            name="room_type",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
