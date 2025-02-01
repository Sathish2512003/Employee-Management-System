from rest_framework import serializers, exceptions
from .models import CustomUser, Employee, LeaveRequest
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model, focusing on key fields like role and email.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = ['id']  # Prevent modification of ID


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model with additional computed full_name field.
    """
    full_name = serializers.SerializerMethodField()
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
                  'department', 'date_joined','position', 'photo']
        read_only_fields = ['id', 'date_joined']  # Ensure date_joined and ID are not editable

    def get_full_name(self, obj):
        """
        Compute the full name of the employee (first_name + last_name).
        """
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        """
        Validate the email field for correct format using Django's built-in email validator.
        """
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value

    def validate_phone_number(self, value):
        """
        Validate phone number for length and numeric characters.
        """
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if value and len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits long.")
        return value

    def validate_photo(self, value):
        """
        Validate the uploaded photo to ensure it's within the size limit.
        """
        max_size = 5 * 1024 * 1024  # 5MB max size
        if value and value.size > max_size:
            raise exceptions.ValidationError("Photo file is too large. Maximum size is 5MB.")
        return value


class LeaveRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for LeaveRequest model with additional employee name field.
    """
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'employee_name', 'start_date', 'end_date', 'leave_type', 'status']
        read_only_fields = ['id', 'status']  # Prevent direct editing of ID and status

    def get_employee_name(self, obj):
        """
        Get the full name of the employee who made the leave request.
        """
        return f"{obj.employee.first_name} {obj.employee.last_name}"

    def validate(self, data):
        """
        Ensure end_date is after start_date and that there are no overlapping leave requests for the employee.
        """
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be earlier than start date.")

        # Check for overlapping leave requests for the same employee
        overlapping_requests = LeaveRequest.objects.filter(
            employee=data['employee'],
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date'],
            status='APPROVED'  # Only check for approved leave requests
        )
        if overlapping_requests.exists():
            raise serializers.ValidationError("Leave request overlaps with an existing approved leave request.")

        return data
