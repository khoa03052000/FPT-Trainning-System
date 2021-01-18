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
    department = models.CharField(default="HR", max_length=20)


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


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(default="khoa@gmail.com")
    phone = models.CharField(max_length=12)
    age = models.IntegerField(default=18)
    dot = models.DateField(default="03/05/2000")
    education = models.CharField(max_length=50)
    experience = models.IntegerField(default=1)
    location = models.CharField(max_length=50)
    toeic_score = models.IntegerField(default=1)
    department = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField()
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
