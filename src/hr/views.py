from django.shortcuts import render
from .models import Vacations, Attendance, SalaryInfo
from account.models import Account
from .serializers import VacationsSerialise, AttendanceSerialise
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import QueryDict
import dateutil.parser
from datetime import datetime, date, timedelta
from post_office import mail

allowed_vacations_count = 15
fixed_days_hours = 8


def home_screen_view(request):

    return render(request, "hr/home.html")


def vacation_editable_list_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        
        try:

            user_vacation = Vacations.objects.filter(user_id=user.id, from_date__year=datetime.now().year, to_date__year=datetime.now().year)
        
        except Exception as e:

            return HttpResponse(e)

        total_used_days = 0

        for interval in user_vacation:
            total_used_days += interval.duration
        
        context['vacations_days'] = allowed_vacations_count
        context['off_days'] = total_used_days
        context['remaining_vacations'] = allowed_vacations_count - total_used_days

    return render(request, "hr/editable_vacations_list.html", context)


def vacation_json_list(request):
    
    user = request.user
    if user.is_authenticated:

        user_id = request.user.id

        try:
            vacations_list = Vacations.objects.filter(user_id=user_id)
            serialise = VacationsSerialise(vacations_list, many=True)
        
        except Exception as e:

            return HttpResponse(e)

        return JsonResponse(serialise.data, safe=False)


def vacation_addition(request):

    user = request.user
    if user.is_authenticated:
        if request.POST:

            user_id = request.user.id
            description = request.POST['description']
            from_date = request.POST['fromDatePicker']
            to_date = request.POST['toDatePicker']

            from_date_parsed = dateutil.parser.parse(from_date)
            to_date_parsed = dateutil.parser.parse(to_date)
            
            string_duration = to_date_parsed - from_date_parsed
            split_duration = str(string_duration).split()
            int_duration = int(split_duration[0])

            try:
                user_vacations = Vacations.objects.filter(user_id=user.id)
            except Exception as e:
                
                return HttpResponse(e)

            total_taken_days = 0

            for vacation in user_vacations:
                total_taken_days += vacation.duration

                if from_date_parsed.date() <= vacation.from_date <= to_date_parsed.date() or from_date_parsed.date() <= vacation.to_date <= to_date_parsed.date():
                    content = {'You Already Took It Off'}
                    return HttpResponse(content, 406)

                if vacation.duration + int_duration >= allowed_vacations_count:

                    content = {f'Your Vacations exceeds {allowed_vacations_count} days'}
                    return HttpResponse(content, 406)

            if total_taken_days >= allowed_vacations_count:
                content = {f'You Cannot exceed {allowed_vacations_count} days'}
                return HttpResponse(content, 406)

            if from_date_parsed.date() <= date.today() or to_date_parsed.date() <= date.today():
                content = {'You Can Only Take Days off Staring Tomorrow'}
                return HttpResponse(content, 406)
            
            if int_duration >= allowed_vacations_count:
                content = {f'The Maximum Allowed is {allowed_vacations_count} days'}
                return HttpResponse(content, 406)

            try:

                create_vacation_object = Vacations.objects.create(
                    description=description,
                    from_date=from_date,
                    to_date=to_date,
                    user_id=user_id,
                    duration=int_duration+1
                )

                last_user_vacation = Vacations.objects.filter(user_id=user_id).last()

                for i in range(0, last_user_vacation.duration):

                    create_attendance_day_off = Attendance.objects.create(
                        user_id=user_id,
                        attended=False,
                        day_off=True,
                        vacation_id=last_user_vacation.id,
                        date_created=datetime.now()
                    )

                content = {'Data Saved Successfully'}
                
                return HttpResponse(content, 200)
            
            except Exception as e:

                return HttpResponse(e)


def vacation_edit(request):

    user = request.user
    if user.is_authenticated:
        if request.method == 'DELETE':
            vacation_id = QueryDict(request.body).get('vacationID')
            
            try:

                user_vacation = Vacations.objects.get(pk=vacation_id)
            except Exception as e:
                
                return HttpResponse(e)

            total_taken_days = 0
            
            if user_vacation.from_date <= date.today() or user_vacation.to_date <= date.today():
                content = {'You Cannot Delete an Old Vacation'}
                return HttpResponse(content, 406)

            try:
                
                content = {'Deleted Successfully'}
                Vacations.objects.filter(pk=vacation_id).delete()

                return HttpResponse(content, 200)

            except Exception as e:
                return HttpResponse(e)


def attendance_list_view(request):
    user = request.user

    context = {}

    if user.is_authenticated:

        try:
            is_checked_in = Attendance.objects.filter(user_id=user.id, check_in__date=datetime.now())
            is_checked_out = Attendance.objects.filter(user_id=user.id, check_out__date=datetime.now())
            user_obj = Account.objects.get(id=user.id)
            hour_rate = user_obj.hour_rate
            context['hour_rate'] = hour_rate
        
        except Exception as e:
            return HttpResponse(e)

        context['is_checked_in'] = False
        context['is_checked_out'] = False

        if is_checked_in:
            context['is_checked_in'] = True

        if is_checked_out:
            context['is_checked_out'] = True
        
        salary_based_on_working_hours,\
            salary_based_on_vacations, \
            overall_salary,\
            month_total_working_hour_count,\
            month_total_off_days = calculate_salary(user.id, hour_rate)

        is_salary_info_exists = SalaryInfo.objects.filter(user_id=user.id, date_created__month=datetime.now().month).count()

        salary_info_object = SalaryInfo.objects.get(user_id=user.id, date_created__month=datetime.now().month)

        if is_salary_info_exists == 1:
            salary_record_id = salary_info_object.id
            try:
                SalaryInfo.objects.filter(pk=salary_record_id).update(
                    salary_based_on_working_hours=format(salary_based_on_working_hours, ".2f"),
                    salary_on_vacations=format(salary_based_on_vacations, ".2f"),
                    overall_salary=format(overall_salary, ".2f"),
                    month_total_working_hour_count=month_total_working_hour_count,
                    month_total_off_days=month_total_off_days,
                    date_updated=datetime.now()
                )

            except Exception as e:
                return HttpResponse(e)
        else:

            try:

                create_salary_object = SalaryInfo.objects.create(
                    user_id=user.id,
                    salary_based_on_working_hours=format(salary_based_on_working_hours, ".2f"),
                    salary_on_vacations=format(salary_based_on_vacations, ".2f"),
                    overall_salary=format(overall_salary, ".2f"),
                    month_total_working_hour_count=month_total_working_hour_count,
                    month_total_off_days=month_total_off_days,
                    date_created=datetime.now(),
                )

            except Exception as e:
                return HttpResponse(e)

        try:

            salary_info_object = SalaryInfo.objects.get(user_id=user.id, date_created__month=datetime.now().month)
            context['salary_info'] = salary_info_object

            # email sender must be scheduled monthly (cron job)

            if datetime.now().day == 1 and salary_info_object.date_updated.day == 1:
                mail.send(
                    user.email,
                    'testingDjangoMailing@gmail.com',
                    template='salaryInfo_email',
                    context=context,
                )

        except Exception as e:
            return HttpResponse(e)

    return render(request, "hr/attendance_list.html", context)


def attendance_json_list(request):

    current_user_id = request.user.id
    try:

        attendance_json_format_list = Attendance.objects.filter(
            user_id=current_user_id,
            check_in__month=datetime.now().month
        )

    except Exception as e:

        return HttpResponse(e)

    serialise = AttendanceSerialise(attendance_json_format_list, many=True)

    return JsonResponse(serialise.data, safe=False)


def check_submit(request):
    req = request.POST

    if req:
        current_user_id = request.user.id
        is_check_in = None
        is_check_out = None

        if req['checkType'] == "CheckIn":
            is_check_in = True 
            
        elif req['checkType'] == "CheckOut":
            is_check_out = True 

        try:
            if is_check_in:
                create_attendance_object = Attendance.objects.create(
                    check_in=datetime.now(),
                    check_out=None,
                    user_id=current_user_id,
                    date_created=datetime.now()
                )

            elif is_check_out:
                
                last_attendance = Attendance.objects.filter(user_id=current_user_id).last()
    
                Attendance.objects.filter(pk=last_attendance.id).update(
                    check_out=datetime.now(),
                    attended=True,
                    day_off=False,
                    vacation_id=None
                )
            
            content = {'Data Saved Successfully'}
            return HttpResponse(content, 200)
        except Exception as e:
            return HttpResponse(e)


def calculate_salary(current_user_id, hour_rate):

    month_total_working_hour_count = 0
    month_total_off_days = 0

    try:

        normal_month_days = Attendance.objects.filter(
            user_id=current_user_id,
            check_in__year=datetime.now().year,
            check_out__month=datetime.now().month,
            attended=True, 
            )

        vacation_month_days = Attendance.objects.filter(
            user_id=current_user_id,
            attended=False,
            day_off=True,
            date_created__month=datetime.now().month,
            )

        user_vacations = Vacations.objects.filter(
            user_id=current_user_id,
            from_date__month=datetime.now().month,
            to_date__month=datetime.now().month
            )
    
    except Exception as e:
        return HttpResponse(e)

    for vacation in user_vacations:
        month_total_vacations_days_number = vacation.duration
        month_total_off_days += month_total_vacations_days_number
        
    for day in normal_month_days:
        day_total_hour = int(day.check_out.hour) - int(day.check_in.hour)
        month_total_working_hour_count += day_total_hour

    salary_based_on_working_hours = month_total_working_hour_count * hour_rate

    salary_based_on_vacations = month_total_off_days * fixed_days_hours * hour_rate
    overall_salary = salary_based_on_working_hours + salary_based_on_vacations
    
    return salary_based_on_working_hours, salary_based_on_vacations, overall_salary, month_total_working_hour_count, month_total_off_days

