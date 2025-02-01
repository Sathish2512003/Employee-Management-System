# employee/routing.py
from django.urls import re_path
from . import consumers

# WebSocket URL pattern for employee real-time updates
websocket_urlpatterns = [
    re_path(r'ws/employee/$', consumers.EmployeeConsumer.as_asgi()),
]
