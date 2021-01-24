from django import forms

from FPT.models import Course, Category, Trainer, Trainee, User, AssignUserToCourse


class CourseCreate(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'image', 'is_visible', "category"]


class CategoryCreate(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'size': 10}),
            'description': forms.TextInput(attrs={'size': 20}),
        }


class AssignCourseCreate(forms.Form):
    course_id = forms.CharField(max_length=100)