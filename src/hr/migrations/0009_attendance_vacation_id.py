# Generated by Django 3.1.4 on 2020-12-15 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_attendance_day_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='vacation_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.vacations'),
        ),
    ]
