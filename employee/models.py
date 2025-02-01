from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='EMPLOYEE')

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Add a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Add a unique related_name
        blank=True
    )

class Employee(models.Model):
    POSITION_CHOICES = [
        ('DEVELOPER', 'Developer'),
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
        ('ANALYST', 'Analyst'),
        ('EMPLOYEE', 'Employee'),  # Default position
    ]

    first_name = models.CharField(max_length=40, db_index=True)  # Reduced max_length
    last_name = models.CharField(max_length=40, db_index=True)   # Reduced max_length
    email = models.EmailField(unique=True, max_length=80, db_index=True)  # Reduced max_length
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=40)  # Reduced max_length
    position = models.CharField(max_length=15, choices=POSITION_CHOICES, default='EMPLOYEE')  # Added position field
    date_joined = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)  # Updated: Added photo field


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('SICK', 'Sick'),
        ('VACATION', 'Vacation'),
    ]
    LEAVE_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)  # Reduced max_length
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='PENDING')  # Reduced max_length

    def __str__(self):
        return f"{self.employee} | {self.leave_type} | {self.status}"
