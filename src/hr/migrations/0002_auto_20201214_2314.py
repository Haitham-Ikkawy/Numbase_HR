# Generated by Django 3.1.4 on 2020-12-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='check_out',
            field=models.DateTimeField(default=None, verbose_name='Check out'),
        ),
    ]
