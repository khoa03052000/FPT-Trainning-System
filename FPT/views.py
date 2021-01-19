from django.shortcuts import render, redirect
from .models import Course, Trainer, Trainee, User, Request
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q


# Create your views here.
def index(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def get_profile(request):
    return render(request, 'registration/profile.html')


def get_dashboard(request):
    user = request.user
    trainers = Trainer.objects.all().count()
    trainees = Trainee.objects.all().count()
    users = User.objects.filter(is_staff=True).count()
    requests = Request.objects.all().count()
    courses = Course.objects.all().count()
    context = {
        'trainers': trainers,
        'trainees': trainees,
        'users': users,
        'requests': requests,
        "user": user,
        "courses": courses
    }
    return render(request, 'index.html', context=context)
