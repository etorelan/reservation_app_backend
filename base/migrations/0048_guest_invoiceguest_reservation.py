# Generated by Django 3.2.8 on 2023-04-15 15:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_auto_20230415_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=30)),
                ('street_name', models.CharField(max_length=100)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_guests', to='base.country')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date_time', models.DateTimeField()),
                ('check_out_date_time', models.DateTimeField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_modified', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('PEND', 'Pending'), ('CNCL', 'Cancelled'), ('CNFR', 'Confirmed')], default='PEND', max_length=4)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_reservations', to='base.guest')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_reservations', to='base.room')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceGuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_issued', models.DateTimeField(auto_now_add=True)),
                ('time_paid', models.DateTimeField()),
                ('time_canceled', models.DateTimeField()),
                ('invoice_amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_invoices', to='base.guest')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_invoices', to='base.reservation')),
            ],
        ),
    ]