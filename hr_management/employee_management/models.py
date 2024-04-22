from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .utils import document_upload_to

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    EDUCATION_LEVEL_CHOICES = (
        ('Master', 'Master\'s Degree'),
        ('Degree', 'Bachelor\'s Degree'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pension_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    is_coc_certified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='employee_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.mobile}"


class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=document_upload_to)
    description = models.TextField(blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('annual_leave', 'Annual Leave'),
        ('sick_leave', 'Sick Leave'),
        ('other_leave', 'Other Leave')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(User, related_name='marked_attendance', on_delete=models.SET_NULL, null=True, blank=True)
    marked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'date',)

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.get_status_display()}"
    

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=(('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')))

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.start_date} to {self.end_date})"
