from django.contrib import admin
from employee_management.models import Position, Department, Employee
# Register your models here.

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)