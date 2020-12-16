from django.contrib import admin
from .models import Vacations, Department


class AdminVacationsView(admin.ModelAdmin):
    list_display = ('description', 'from_date', 'to_date', 'duration', 'duration', 'user_id')
    search_fields = ('description', 'from_date', 'to_date', 'duration', 'duration', 'user_id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Vacations, AdminVacationsView)


class AdminDepartmentView(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Department, AdminDepartmentView)

