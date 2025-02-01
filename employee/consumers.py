# employee/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import socketio

# Initialize Socket.IO client
sio = socketio.Client()

# Create a Django Channels Consumer to handle WebSocket connections
class EmployeeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # This group will be used to send real-time messages
        self.room_group_name = "employee_notifications"

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Connect the Socket.IO client
        sio.connect("http://localhost:5000")  # Adjust the Socket.IO server URL

        # Define callback functions to handle Socket.IO events
        sio.on('newEmployee')(self.new_employee_event)
        sio.on('newLeaveRequest')(self.new_leave_request_event)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Disconnect the Socket.IO client when WebSocket connection is closed
        sio.disconnect()

    # Define a method to handle the 'newEmployee' event from Socket.IO
    def new_employee_event(self, employee):
        # Send the employee event data to WebSocket clients
        self.send(text_data=json.dumps({
            "event": "newEmployee",
            "data": employee
        }))

    # Define a method to handle the 'newLeaveRequest' event from Socket.IO
    def new_leave_request_event(self, leave_request):
        # Send the leave request event data to WebSocket clients
        self.send(text_data=json.dumps({
            "event": "newLeaveRequest",
            "data": leave_request
        }))
