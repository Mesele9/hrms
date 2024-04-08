from django import forms
from .models import Employee, Department, Position


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
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'department', 'position', 'date_of_birth', 'hire_date', 'salary', 'is_active', 'picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # Update initial data for existing instance
            self.fields['department'].queryset = Department.objects.all()
            self.fields['position'].queryset = Position.objects.all()