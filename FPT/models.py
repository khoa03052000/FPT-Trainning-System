from datetime import timedelta

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
    department = models.CharField(default="FPT", max_length=20, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True)
    full_name = models.CharField(max_length=50, default="", blank=True)
    role = models.CharField(max_length=10, default="", blank=True)

    def save(self, *args, **kwargs):
        if len(self.full_name) == 0:
            self.full_name = self.last_name + self.first_name

        if self.is_superuser and self.is_staff:
            self.role = "Admin"
            self.department = "FPT Co."
        elif self.is_staff:
            self.role = "Staff"
            self.department = "HR"
        elif self.is_trainer:
            self.role = "Trainer"
            self.department = "FPT Education"
            trainer = Trainer.objects.filter(user=self)
            if trainer.exists() is False:
                Trainer.objects.create(user=self)
        elif self.is_trainee:
            self.role = "Trainee"
            self.department = "FPT Education"
        return super().save(*args, **kwargs)


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    education = models.CharField(max_length=50, default="", blank=True, null=True)
    phone = models.CharField(max_length=12, default="", blank=True, null=True)
    working_place = models.CharField(max_length=50, default="", blank=True, null=True)
    type = models.CharField(max_length=2, choices=TYPE_DEPARTMENT, default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=12, default="", blank=True, null=True)
    age = models.IntegerField(default=18, blank=True, null=True)
    dot = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=50, default="",null=True, blank=True)
    experience = models.IntegerField(default=1, null=True, blank=True)
    location = models.CharField(max_length=50, default="", null=True, blank=True)
    toeic_score = models.IntegerField(default=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ManyToManyField(Category)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AssignUserToCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_assign")
    assigned_user_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True,
        related_name="user_type"
    )
    assigned_user_id = models.BigIntegerField(null=True, blank=True)
    assigned_user = GenericForeignKey("assigned_user_type", "assigned_user_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assigned_user} in {self.course.name}"

    def save(self, *args, **kwargs):
        if self.assigned_user_id:
            if self.assigned_user_type.id == 7:
                trainer = Trainer.objects.filter(pk=self.assigned_user_id)
                if trainer.exists():
                    return super().save(*args, **kwargs)
            elif self.assigned_user_type.id == 8:
                trainee = Trainee.objects.filter(pk=self.assigned_user_id)
                if trainee.exists():
                    return super().save(*args, **kwargs)


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
    is_permission = models.BooleanField(default=False, null=False)
    limit_time = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(default="khoa@gmail.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Request from {self.user.username} to {self.course.name}"

    def save(self, *args, **kwargs):
        if self.status == 'APPROVED':
            self.is_permission = True
            if self.updated_at is not None:
                self.limit_time = self.updated_at + timedelta(days=7)
                return super().save(*args, **kwargs)
        elif self.status == 'REJECTED':
            self.limit_time = None
            self.is_permission = False
            return super().save(*args, **kwargs)
        elif self.status == 'CANCELLED':
            self.delete()
        else:
            return super().save(*args, **kwargs)

