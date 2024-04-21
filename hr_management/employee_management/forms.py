from django import forms
from django.forms import inlineformset_factory
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
    class Meta:
        model = Attendance
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    

class AttendanceBulkForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.filter(is_active=True), widget=forms.CheckboxSelectMultiple)
    status = forms.ChoiceField(choices=Attendance.STATUS_CHOICES, widget=forms.RadioSelect)

class EmployeeFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    search = forms.CharField(required=False)


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
