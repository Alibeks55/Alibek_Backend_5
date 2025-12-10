from django.db import models
from django.contrib.auth.models import User

class UsersCod(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
