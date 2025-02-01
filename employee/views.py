import socketio
import logging
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, LeaveRequestSerializer
from django.shortcuts import get_object_or_404

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize the Socket.IO client
sio = socketio.Client()

# Connect to the Socket.IO server
try:
    sio.connect('http://localhost:5000')  # Replace with your Socket.IO server URL
    logger.info("Successfully connected to Socket.IO server.")
except socketio.exceptions.ConnectionError as e:
    logger.error(f"Failed to connect to Socket.IO server: {e}")

class EmployeeListCreate(APIView):
    """
    API View to handle GET (list) and POST (create) requests for Employee model.
    """
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_employee = serializer.data

            # Emit the 'newEmployee' event to Socket.IO server
            try:
                if sio.connected:
                    sio.emit('newEmployee', new_employee)
                    logger.info("Emitted 'newEmployee' event successfully.")
                else:
                    logger.warning("Socket.IO server not connected. Event emission skipped.")
            except Exception as e:
                logger.error(f"Error emitting 'newEmployee' event: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(APIView):
    """
    API View to handle admin login requests.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:  # Ensure the user is an admin
            return Response({"message": "Login successful", "is_admin": True}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials or not an admin"}, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeDetailUpdateDelete(APIView):
    """
    API View to handle GET (retrieve), PUT (update), and DELETE (destroy) requests for a single Employee.
    """
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            updated_employee = serializer.data

            # Emit the 'employeeUpdated' event to Socket.IO server
            try:
                if sio.connected:
                    sio.emit('employeeUpdated', updated_employee)
                    logger.info("Emitted 'employeeUpdated' event successfully.")
                else:
                    logger.warning("Socket.IO server not connected. Event emission skipped.")
            except Exception as e:
                logger.error(f"Error emitting 'employeeUpdated' event: {e}")

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()

        # Emit the 'employeeDeleted' event to Socket.IO server
        try:
            if sio.connected:
                sio.emit('employeeDeleted', {"id": pk})
                logger.info("Emitted 'employeeDeleted' event successfully.")
            else:
                logger.warning("Socket.IO server not connected. Event emission skipped.")
        except Exception as e:
            logger.error(f"Error emitting 'employeeDeleted' event: {e}")

        return Response({"detail": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LeaveRequestListCreate(APIView):
    """
    API View to handle GET (list) and POST (create) requests for LeaveRequest model.
    """
    def get(self, request):
        leaves = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_leave_request = serializer.data

            # Emit the 'newLeaveRequest' event to Socket.IO server
            try:
                if sio.connected:
                    sio.emit('newLeaveRequest', new_leave_request)
                    logger.info("Emitted 'newLeaveRequest' event successfully.")
                else:
                    logger.warning("Socket.IO server not connected. Event emission skipped.")
            except Exception as e:
                logger.error(f"Error emitting 'newLeaveRequest' event: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestDetailUpdateDelete(APIView):
    """
    API View to handle GET (retrieve), PUT (update), and DELETE (destroy) requests for a single LeaveRequest.
    """
    def get(self, request, pk):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        serializer = LeaveRequestSerializer(leave_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        # Get status from request data (if available)
        status = request.data.get("status")
        if status:
            leave_request.status = status  # Update the status explicitly
            leave_request.save()

        serializer = LeaveRequestSerializer(leave_request)
        updated_leave_request = serializer.data

        # Emit the 'leaveRequestUpdated' event to Socket.IO server
        try:
            if sio.connected:
                sio.emit('leaveRequestUpdated', updated_leave_request)
                logger.info("Emitted 'leaveRequestUpdated' event successfully.")
            else:
                logger.warning("Socket.IO server not connected. Event emission skipped.")
        except Exception as e:
            logger.error(f"Error emitting 'leaveRequestUpdated' event: {e}")

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        leave_request = get_object_or_404(LeaveRequest, pk=pk)
        leave_request.delete()

        # Emit the 'leaveRequestDeleted' event to Socket.IO server
        try:
            if sio.connected:
                sio.emit('leaveRequestDeleted', {"id": pk})
                logger.info("Emitted 'leaveRequestDeleted' event successfully.")
            else:
                logger.warning("Socket.IO server not connected. Event emission skipped.")
        except Exception as e:
            logger.error(f"Error emitting 'leaveRequestDeleted' event: {e}")

        return Response({"detail": "Leave request deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
