from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    
    
    def __str__(self):
        return self.username