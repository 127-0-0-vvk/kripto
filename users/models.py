from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ForgotPasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    token = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    