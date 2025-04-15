from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png')
    created_at = models.DateTimeField(auto_now_add=True)  # Adds the created_at field
    status = models.CharField(max_length=20, choices=[('Busy', 'Busy'), ('Available', 'Available')], default='Available')
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

