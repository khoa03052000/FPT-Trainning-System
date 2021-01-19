from django.shortcuts import render, redirect
from .models import Course
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q


# Create your views here.
def index(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})