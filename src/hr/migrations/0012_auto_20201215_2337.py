# Generated by Django 3.1.4 on 2020-12-15 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0011_attendance_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 15, 23, 37, 38, 540758), verbose_name='date created'),
        ),
    ]
