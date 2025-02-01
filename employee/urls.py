from django.urls import path
from .views import (
    EmployeeListCreate, EmployeeDetailUpdateDelete,
    LeaveRequestListCreate, LeaveRequestDetailUpdateDelete
)

urlpatterns = [
    path('employees/', EmployeeListCreate.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailUpdateDelete.as_view(), name='employee-detail'),
    path('leave-requests/', LeaveRequestListCreate.as_view(), name='leave-request-list-create'),
    path('leave-requests/<int:pk>/', LeaveRequestDetailUpdateDelete.as_view(), name='leave-request-detail'),
]
