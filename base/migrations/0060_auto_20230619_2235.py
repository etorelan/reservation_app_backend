# Generated by Django 3.2.8 on 2023-06-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0059_alter_roomtype_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]