from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_screen_view, name="home"),


    path('vacationsManipulation/', views.vacation_editable_list_view,
         name="vacationsManipulation"),

    # returns JSON Response (GET)
    path('vacations/vacations', views.vacation_json_list, name="vacations"),

    # for vacations manipulation
    path('vacations/vacationAddition/', views.vacation_addition, name="vacationAddition"),

    path('vacations/vacationEdit/', views.vacation_edit, name="vacationEdit"),

    path('attendanceListView/', views.attendance_list_view, name="attendanceListView"),

    path('attendance_json_list/', views.attendance_json_list, name="attendance_json_list"),

    path('submitCheck/', views.check_submit, name="submitCheck"),
]
