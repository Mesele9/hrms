from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Department, Position, Document, LeaveRequest
from .forms import EmployeeForm, DepartmentForm, PositionForm, DocumentForm, LeaveRequestForm

def home(request):
    return render(request, 'home.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hrms:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

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

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('hrms:employee_list')

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hrms:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})

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

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('hrms:department_list')

def position_list(request):
    positions = Position.objects.all()
    return render(request, 'position_list.html', {'positions': positions})

def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hrms:position_list')
    else:
        form = PositionForm()
    return render(request, 'position_form.html', {'form': form})

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

def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.delete()
    return redirect('hrms:position_list')

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'document_form.html', {'form': form})

def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_form.html', {'form': form})

def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    return redirect('document_list')

def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'leave_request_list.html', {'leave_requests': leave_requests})

def leave_request_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_request_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_request_form.html', {'form': form})

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

def leave_request_delete(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.delete()
    return redirect('leave_request_list')
