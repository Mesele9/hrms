
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    employee_list, employee_create, employee_update, employee_delete, employee_detail,
    department_list, department_create, department_update, department_delete,
    position_list, position_create, position_update, position_delete, 
    document_list, document_create, document_update, document_delete, 
    leave_request_list, leave_request_create, leave_request_update, leave_request_delete,
)

app_name = 'hrms'

urlpatterns = [
    # Employee Management
    path('employees/', employee_list, name='employee_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('employees/update/<int:pk>/', employee_update, name='employee_update'),
    path('employees/delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('employees/detail/<int:pk>/', employee_detail, name='employee_detail'),

    # Department Management
    path('departments/', department_list, name='department_list'),
    path('departments/create/', department_create, name='department_create'),
    path('departments/update/<int:pk>/', department_update, name='department_update'),
    path('departments/delete/<int:pk>/', department_delete, name='department_delete'),
    #path('departments/detail/<int:pk>/', department_detail, name='department_detail'),

    # Position Management
    path('positions/', position_list, name='position_list'),
    path('positions/create/', position_create, name='position_create'),
    path('positions/update/<int:pk>/', position_update, name='position_update'),
    path('positions/delete/<int:pk>/', position_delete, name='position_delete'),
    #path('positions/detail/<int:pk>/', position_detail, name='position_detail'),

    # Document Management
    path('documents/', document_list, name='document_list'),
    path('documents/create/', document_create, name='document_create'),
    path('documents/update/<int:pk>/', document_update, name='document_update'),
    path('documents/delete/<int:pk>/', document_delete, name='document_delete'),
    #path('documents/detail/<int:pk>/', document_detail, name='document_detail'),

    # Leave Management
    path('leave_requests/', leave_request_list, name='leave_request_list'),
    path('leave_requests/create/', leave_request_create, name='leave_request_create'),
    path('leave_requests/update/<int:pk>/', leave_request_update, name='leave_request_update'),
    path('leave_requests/delete/<int:pk>/', leave_request_delete, name='leave_request_delete'),
    #path('leave_requests/detail/<int:pk>/', leave_request_detail, name='leave_request_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
