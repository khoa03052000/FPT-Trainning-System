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
    department = models.CharField(default="FPT", max_length=20)
    avatar = models.ImageField(null=True, blank=True)
    full_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=10, default="", blank=True)

    def save(self, *args, **kwargs):
        if len(self.full_name) == 0:
            self.full_name = self.last_name + self.first_name

        if self.is_superuser and self.is_staff:
            self.role = "Admin"
        elif self.is_staff:
            self.role = "Staff"
        elif self.is_trainer:
            self.role = "Trainer"
        elif self.is_trainee:
            self.role = "Trainee"
        return super().save(*args, **kwargs)


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    education = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=12, default="", blank=True)
    working_place = models.CharField(max_length=50, default="", blank=True)
    type = models.CharField(max_length=2, choices=TYPE_DEPARTMENT, default='ET')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=12, default="09xx", blank=True)
    age = models.IntegerField(default=18, blank=True)
    dot = models.DateField(default="2000-05-03", blank=True)
    education = models.CharField(max_length=50, default="FPT Education", blank=True)
    experience = models.IntegerField(default=1, blank=True)
    location = models.CharField(max_length=50, default="Da Nang", blank=True)
    toeic_score = models.IntegerField(default=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


