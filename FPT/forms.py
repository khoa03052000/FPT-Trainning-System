from django import forms

from FPT.models import Course


class CourseCreate(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'image', 'is_visible']