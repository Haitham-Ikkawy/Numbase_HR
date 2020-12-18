from django.db import models
from account.models import Account
from datetime import datetime


class Vacations(models.Model):

    auto_increment_id = models.AutoField
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    description = models.CharField(max_length=60)
    from_date = models.DateField('From Date')
    to_date = models.DateField('To Date')
    duration = models.IntegerField(null=True)

    # return the vacation description as a default attribute
    def __str__(self):
        return self.description

# those meta variables to be displayed in the admin panel
    class Meta:
        verbose_name = "Vacations"
        verbose_name_plural = "Employee Vacations"


class Attendance(models.Model):
    auto_increment_id = models.AutoField
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    vacation = models.ForeignKey(Vacations, on_delete=models.CASCADE, null=True)
    check_in = models.DateTimeField('Check In', null=True)
    check_out = models.DateTimeField('Check out', null=True)
    date_created = models.DateTimeField('date created', default=datetime.now())
    attended = models.BooleanField('attended', null=True)
    day_off = models.BooleanField('attended', null=True)

    def __str__(self):
        return self.auto_increment_id

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Employee Attendance"


class SalaryInfo(models.Model):

    auto_increment_id = models.AutoField
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    salary_based_on_working_hours = models.FloatField()
    salary_on_vacations = models.FloatField()
    overall_salary = models.FloatField()
    month_total_working_hour_count = models.IntegerField()
    month_total_off_days = models.IntegerField()
    date_created = models.DateTimeField('date created', default=datetime.now())
    date_updated = models.DateTimeField('date updated', null=True)

    class Meta:
        verbose_name = "SalaryInfo"
        verbose_name_plural = "Employee SalaryInfo"


class Department(models.Model):

    auto_increment_id = models.AutoField
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Employee Department"
