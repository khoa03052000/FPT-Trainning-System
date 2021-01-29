from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.models import Course, Trainer, Trainee, Request, AssignUserToCourse

User = get_user_model()


def index(request):
    return redirect('login')


@require_http_methods(["GET"])
@login_required
def get_dashboard(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        messages.error(request, "User will be blocked by Admin")
        return redirect('login')
    user_courses = AssignUserToCourse.objects.filter(assigned_user_id=user.id)
    if user.is_staff or user.is_superuser:
        trainers = Trainer.objects.all().count()
        trainees = Trainee.objects.all().count()
        staffs = User.objects.filter(is_staff=True).count()
        requests = Request.objects.all().count()
        courses = Course.objects.all().count()
        context = {
            'trainers': trainers,
            'trainees': trainees,
            'staffs': staffs,
            'requests': requests,
            "user": user,
            "courses": courses
        }
        return render(request, 'index.html', context=context)
    if user.is_trainee:
        courses = Course.objects.filter(pk__in=[i.course_id for i in user_courses])
        requests = Request.objects.filter(user=user)
        courses_available = Course.objects.exclude(pk__in=[i.course_id for i in user_courses]).exclude(is_visible=False)
        context = {
            "user": user,
            "courses": courses,
            'requests': requests,
            'courses_available': courses_available
        }
        return render(request, 'index.html', context)
    if user.is_trainer:
        context = {
            "user": user,
        }
        return render(request, 'index.html', context)
    messages.error(request, "You have no role in system")
    return redirect('login')

