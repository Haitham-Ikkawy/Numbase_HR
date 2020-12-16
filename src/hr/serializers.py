from rest_framework import serializers
from .models import Vacations, Attendance


class VacationsSerialise(serializers.ModelSerializer):

    class Meta:
        model = Vacations
        fields = ('id', 'description', 'from_date', 'to_date', 'duration')


class AttendanceSerialise(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'check_in', 'check_out', 'user_id')
