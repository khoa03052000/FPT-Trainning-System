from django.contrib.auth.models import AbstractUser
from django.db import models

TYPE_DEPARTMENT = [
    ('ET', 'External Type'),
    ('IT', 'Internal Type'),
]


# Create your models here.
class User(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    is_trainee = models.BooleanField(default=False)


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    working_place = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=TYPE_DEPARTMENT, default='ET')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
