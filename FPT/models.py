from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    is_trainee = models.BooleanField(default=False)
