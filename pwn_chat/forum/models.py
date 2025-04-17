from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages',null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
