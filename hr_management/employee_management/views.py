import re
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import Employee, Department, Position, Document, Attendance, LeaveRequest
from .forms import EmployeeForm, DepartmentForm, PositionForm, DocumentForm, AttendanceForm, LeaveRequestForm


def home(request):
    if request.user.is_authenticated:
        # Get the user's full name
        full_name = request.user.get_full_name() if request.user.get_full_name() else request.user.username
        print(full_name)
        # Get the current date in a formatted string
        today_date = datetime.today().strftime("%B %d, %Y")

        # Render the home template with user data and today's date
        return render(request, 'home.html', {'user': request.user, 'today_date': today_date})
    else:
        # Render the home template without user data if not authenticated
        return render(request, 'home.html', {'user': None})


@login_required
def dashboard(request):
    # Total number of employees
    active_employees = Employee.objects.filter(is_active=True)
    total_employees = Employee.objects.filter(is_active=True).count()

    # Employees by department
    department_data = active_employees.values('department__name').annotate(employee_count=Count('id'))

    # Employees by gender
    male_count = active_employees.filter(gender='M').count()
    female_count = active_employees.filter(gender='F').count()
    
    today = datetime.today()
    next_week = today + timedelta(days=7)
    upcoming_birthdays = Employee.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day__in=range(today.day, next_week.day)
    ).order_by('-date_of_birth')

    
    context = {
        'department_data': department_data,
        'total_employees': total_employees,
        'male_count': male_count,
        'female_count': female_count,
        'upcoming_birthdays': upcoming_birthdays
    }

    return render(request, 'dashboard.html', context)


@login_required
def employee_list(request):
    all_employees = Employee.objects.all()
    active_employees = all_employees.filter(is_active=True)
    inactive_employees = all_employees.filter(is_active=False)
    
    departments = Department.objects.all()    
    
    status_filter = request.GET.get('status', 'active')
    if status_filter == 'inactive':
        employees = inactive_employees
    elif status_filter == 'all':
        employees = all_employees
    else:
        employees = active_employees

    context = {
        'employees': employees,
        'departments': departments,
        'status_filter': status_filter,
    }
    
    return render(request, 'employee_list.html', context)


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hrms:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('hrms:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('hrms:employee_list')


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    documents = Document.objects.filter(employee=employee)
    next_employee = Employee.objects.filter(is_active=True, id__gt=pk).order_by('pk').first()  # Get the next employee
    previous_employee = Employee.objects.filter(is_active=True, id__lt=employee.id).order_by('-pk').first() # Get the previous employee
    context = {'employee': employee,'previous_employee': previous_employee, 'next_employee': next_employee, 'documents': documents}
    return render(request, 'employee_detail.html', context)    


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hrms:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('hrms:department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('hrms:department_list')


@login_required
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'position_list.html', {'positions': positions})


@login_required
def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hrms:position_list')
    else:
        form = PositionForm()
    return render(request, 'position_form.html', {'form': form})


@login_required
def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('hrms:position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'position_form.html', {'form': form})


@login_required
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    return redirect('hrms:position_list')


@login_required
def document_list(request):
    documents = Document.objects.all()
    employee = Employee.objects.first()  # Example: Get the first employee

    search_query = request.GET.get('search_query')
    if search_query:
        documents = documents.filter(name__icontains=search_query)

    return render(request, 'document_list.html', {'documents': documents, 'employee': employee})


def document_create(request, employee_id=None):
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        # Creating a document from the employee detail page
        return document_upload_form(request, include_employee_field=False, employee=employee)
    else:
        # Creating a document from the document list page (require employee selection)
        return document_upload_form(request, include_employee_field=True)


@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('hrms:document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_form.html', {'form': form})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    return redirect('hrms:document_list')


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'document_detail.html', {'document': document})


@login_required
def document_upload_form(request, include_employee_field=True, employee=None):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, include_employee_field=include_employee_field)
        if form.is_valid():
            form.save()
            return redirect('hrms:document_list')
    else:
        form = DocumentForm(include_employee_field=include_employee_field)

    if employee:
        context = {
            'employee': employee,
            'form': form,
        }
    else:
        context = {
            'form': form,
        }
    return render(request, 'document_upload_form.html', context)


""" @login_required
def document_upload_form(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hrms:document_list')
    else:
        form = DocumentForm()

    # Optionally, you can filter employees to display in the upload form
    employees = Employee.objects.filter(is_active=True)

    context = {
        'form': form,
        'employees': employees,
    }
    return render(request, 'document_upload_form.html', context)
 """

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.employee = Employee.objects.get(pk=form.cleaned_data['employee'].id)
            attendance.save()
            messages.success(request, 'Attendance record created successfully.')
            return redirect('hrms:attendance_list')
    else:
        form = AttendanceForm()

    #employees = Employee.objects.filter(is_active=True)
    
    context = {
        'form': form,
    }

    return render(request, 'attendance_form.html', context)


def attendance_list(request):
    attendances = Attendance.objects.all()

    context = {
        'attendances': attendances,
    }

    return render(request, 'attendance_list.html', context)


def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record updated successfully.')
            return redirect('hrms:attendance_list')
    else:
        form = AttendanceForm(instance=attendance)

    context = {
        'form': form,
        'attendance': attendance,
    }

    return render(request, 'attendance_form.html', context)

def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()
    messages.success(request, 'Attendance record deleted successfully.')
    return redirect('hrms:attendance_list')



@login_required
def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'leave_request_list.html', {'leave_requests': leave_requests})


@login_required
def leave_request_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_request_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_request_form.html', {'form': form})


@login_required
def leave_request_update(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            return redirect('leave_request_list')
    else:
        form = LeaveRequestForm(instance=leave_request)
    return render(request, 'leave_request_form.html', {'form': form})


@login_required
def leave_request_delete(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.delete()
    return redirect('leave_request_list')
