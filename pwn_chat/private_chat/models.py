from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='private_sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='private_received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.text[:30]}"
