from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    assigned_user_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True,
        related_name="user_type"
    )
    assigned_user_id = models.BigIntegerField(null=True, blank=True)
    assigned_user = GenericForeignKey("assigned_user_type", "assigned_user_id")
    name = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    image = models.ImageField()
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_request")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_request")
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELLED, 'Cancelled'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    email = models.EmailField(default="khoa@gmail.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


