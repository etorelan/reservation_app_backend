# Generated by Django 3.2.8 on 2023-04-11 20:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_reservation_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 11, 21, 10, 35, 429089, tzinfo=utc)),
        ),
    ]
