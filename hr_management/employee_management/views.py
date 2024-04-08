from django.shortcuts import render, redirect
from .models import Employee, Department, Position
from .forms import EmployeeForm, DepartmentForm, PositionForm

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return redirect('employee_list')

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})

def department_update(request, pk):
    department = Department.objects.get(pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})

def department_delete(request, pk):
    department = Department.objects.get(pk=pk)
    department.delete()
    return redirect('department_list')

def position_list(request):
    positions = Position.objects.all()
    return render(request, 'position_list.html', {'positions': positions})

def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position_list')
    else:
        form = PositionForm()
    return render(request, 'position_form.html', {'form': form})

def position_update(request, pk):
    position = Position.objects.get(pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'position_form.html', {'form': form})

def position_delete(request, pk):
    position = Position.objects.get(pk=pk)
    position.delete()
    return redirect('position_list')
