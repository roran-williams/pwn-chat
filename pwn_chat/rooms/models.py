from django.db import models
from django.conf import settings

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=32, default='open')
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
