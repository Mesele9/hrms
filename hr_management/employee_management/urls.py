from django.urls import path
from . import views

urlpatterns = [
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/update/<int:pk>/', views.employee_update, name='employee_update'),
    path('employee/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('department/list/', views.department_list, name='department_list'),
    path('department/create/', views.department_create, name='department_create'),
    path('department/update/<int:pk>/', views.department_update, name='department_update'),
    path('department/delete/<int:pk>/', views.department_delete, name='department_delete'),
    path('position/list/', views.position_list, name='position_list'),
    path('position/create/', views.position_create, name='position_create'),
    path('position/update/<int:pk>/', views.position_update, name='position_update'),
    path('position/delete/<int:pk>/', views.position_delete, name='position_delete'),
]
