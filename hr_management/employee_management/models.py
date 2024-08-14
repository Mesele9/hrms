from django.db import models
from django.contrib.auth.models import User
from datetime import date
from .utils import document_upload_to
from ethiopian_date import EthiopianDateConverter
from django.utils import timezone
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):

    et_calendar = EthiopianDateConverter()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    EDUCATION_LEVEL_CHOICES = (
        ('Master', 'Master\'s Degree'),
        ('Degree', 'Bachelor\'s Degree'),
        ('Diploma', 'Diploma'),
        ('Certificate', 'Certificate'),
        ('Grade', 'Grade'),
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
    accrued_annual_leave = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    used_annual_leave = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)


    def __str__(self):
        return f"{self.first_name} {self.middle_name}"
    
    # Convert date of birth to gregorian date
    def gregorian_date_of_birth(self):
        if self.date_of_birth:
            ethiopian_date = self.date_of_birth
            converted_date = self.et_calendar.to_gregorian(ethiopian_date.year, ethiopian_date.month, ethiopian_date.day)
        else:
            None
        return converted_date
    
    # convert hire date to gregorian date
    def gregorian_hire_date(self):
        if self.hire_date:
            ethiopian_date = self.hire_date
            converted_date = self.et_calendar.to_gregorian(ethiopian_date.year, ethiopian_date.month, ethiopian_date.day)
        else:
            None
        return converted_date

    def update_annual_leave_balance(self):
        today = timezone.now().date()
        hire_date_gregorian = self.gregorian_hire_date()
        tenure_days = (today - hire_date_gregorian).days

        if tenure_days >= 182:  # Employee is eligible after 6 months (approx 182 days)
            full_years = tenure_days // 365
            remaining_days = tenure_days % 365

            leave_days = 0

            if full_years > 0:
                leave_days += 16  # First year accrual
                for year in range(1, full_years):
                    leave_days += 16 + 0.5 * year

            # Calculate the leave accrued for the remaining days
            if remaining_days > 0:
                increment = 16 + 0.5 * full_years
                leave_days += (remaining_days / 365) * increment

            self.accrued_annual_leave = leave_days
            self.save()
    
    #@property
    def get_annual_leave_balance(self):
        return self.accrued_annual_leave - self.used_annual_leave


class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LeaveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.leave_type.name} - {self.start_date} : {self.start_date} - {self.status}"
    
    def get_total_days(self):
        total_days = (self.end_date - self.start_date).days + 1
        return total_days


    def save(self, *args, **kwargs):
        if self.status == 'approved':
            self.employee.used_annual_leave += self.get_total_days()
            self.employee.save()
        super().save(*args, **kwargs)    

class Document(models.Model):

    NAME_CHOICES = (
        ('educational_document', 'Educational Document'),
        ('kebele_id', 'Kebele ID'),
        ('employment', 'Employement Letter'),
        ('promotion', 'Promotions Letter'),
        ('demotion', 'Demotion Letter'),
        ('first_warning', 'First Warning'),
        ('second_warning', 'Second Warning'),
        ('third_warning', 'Third Warning'),
        ('final_warning', 'Second Warning'),
        ('termination', 'Termination Letter'),    
    )
    name = models.CharField(max_length=100, choices=NAME_CHOICES)
    file = models.FileField(upload_to=document_upload_to)
    description = models.TextField(blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

