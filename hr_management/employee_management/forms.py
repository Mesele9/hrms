from django import forms
from .models import Employee, Department, Position, Document, Attendance, LeaveRequest


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'email', 'department', 'position', 'date_of_birth', 'hire_date', 'salary', 'is_active', 'picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file', 'description', 'employee']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        include_employee_field = kwargs.pop('include_employee_field', True)
        super().__init__(*args, **kwargs)

        if not include_employee_field:
            self.fields.pop('employee')  # Remove 'employee' field if not needed
        else:
            self.fields['employee'].queryset = Employee.objects.filter(is_active=True)



class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter employee choices to only include active employees
        self.fields['employee'].queryset = Employee.objects.filter(is_active=True)

    class Meta:
        model = Attendance
        fields = ('employee', 'date', 'status')
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


""" class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('employee', 'date', 'status')
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

 """
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
