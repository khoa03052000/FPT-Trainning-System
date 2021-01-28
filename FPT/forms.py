from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from FPT.models import Course, Category, Trainer, Trainee

User = get_user_model()


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "department", "avatar"]


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = [
            "education",
            "phone",
            "working_place",
            "type",
        ]


class TraineeForm(forms.ModelForm):
    class Meta:
        model = Trainee
        fields = [
            "phone",
            "age",
            "dot",
            "education",
            "location",
            "toeic_score",
            "experience"
        ]


ROLE_CHOICES = [
    ('trainee', 'Trainee'),
]


class UserFPTCreationForm(UserCreationForm):
    roles = forms.CharField(label='Choose role', widget=forms.Select(choices=ROLE_CHOICES))

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserFPTCreationForm, self).save(commit=True)
        user.is_trainee = True
        user_info = Trainee(user=user)
        user_info.save()
        user.save()
        return user, user_info
