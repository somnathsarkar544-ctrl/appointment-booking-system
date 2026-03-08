from datetime import time

from django.db import models
from accounts.models import User

# Create your models here.

class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    experience = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    start_time = models.TimeField(default=time(9, 0))  # Default start time 9:00 AM
    end_time = models.TimeField(default=time(17, 0))   # Default end time 5:00 PM
    

    def __str__(self):
        return self.name
   