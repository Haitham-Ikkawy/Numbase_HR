# Generated by Django 3.1.4 on 2020-12-15 21:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_auto_20201215_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='date_created',
            field=models.DateField(default=datetime.date(2020, 12, 15), verbose_name='date created'),
        ),
    ]
