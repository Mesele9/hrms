from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from employee_management.models import Position, Department, Employee

# Register your models here.


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'email', 'department', 'position', 'date_of_birth', 'hire_date', 'salary')


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ('first_name', 'middle_name', 'last_name', 'gender', 'email', 'department', 'position', 'date_of_birth', 'hire_date', 'salary')

    list_filter = ('department', 'position', 'gender', 'is_active')
    search_fields = ('first_name', 'last_name', 'department__name', 'position__name')
    ordering = ('first_name', 'last_name')

#admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Position)