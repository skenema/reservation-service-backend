# Generated by Django 4.2 on 2023-04-12 13:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_service', '0003_alter_seat_show_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='show_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 12, 13, 34, 36, 802657)),
        ),
    ]
