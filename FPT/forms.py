from django import forms

from FPT.models import Course, Category, Trainer, Trainee, User


class CourseCreate(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'image', 'is_visible']


class CategoryCreate(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"