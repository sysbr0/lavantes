from django.db import models
from django.conf import settings
from django.utils.timezone import now
from employe.models import *

class ChatMessage(models.Model):
    sender_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Admins are still part of AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='sent_admin_messages',
        null=True,  # Sender can be null if the employee is sending
        blank=True
    )
    sender_employee = models.ForeignKey(
        Employee,  # Reference to your Employee model
        on_delete=models.CASCADE,
        related_name='sent_employee_messages',
        null=True,  # Sender can be null if the admin is sending
        blank=True
    )
    receiver_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_admin_messages',
        null=True,  # Receiver can be null if the employee is receiving
        blank=True
    )
    receiver_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='received_employee_messages',
        null=True,  # Receiver can be null if the admin is receiving
        blank=True
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.sender_admin:
            sender = f"Admin {self.sender_admin}"
        else:
            sender = f"Employee {self.sender_employee}"
        if self.receiver_admin:
            receiver = f"Admin {self.receiver_admin}"
        else:
            receiver = f"Employee {self.receiver_employee}"
        return f"From {sender} to {receiver} at {self.timestamp}"
