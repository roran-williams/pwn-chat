from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Status(models.Model):
    name = models.CharField(max_length=32)
    is_default = models.BooleanField(default=False)
    hide_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=28,null=False,unique=True)
    desc = models.TextField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)  # Use ForeignKey to Status

    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='room_created', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name 

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='private_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='private_received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.text[:30]}"
