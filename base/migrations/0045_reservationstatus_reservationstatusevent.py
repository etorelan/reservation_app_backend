# Generated by Django 3.2.8 on 2023-04-15 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_auto_20230415_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationStatus',
            fields=[
                ('name', models.CharField(choices=[('PEND', 'Pending'), ('CNCL', 'Cancelled'), ('CNFR', 'Confirmed')], max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationStatusEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_events', to='base.reservation')),
                ('reservation_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_status_events', to='base.reservationstatus')),
            ],
        ),
    ]
