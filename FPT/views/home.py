from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from FPT.models import Course, Trainer, Trainee, User, Request, AssignUserToCourse


def index(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


@require_http_methods(["GET"])
@login_required
def get_dashboard(request):
    user = request.user
    user_courses = AssignUserToCourse.objects.filter(assigned_user_id=user.id)
    courses = Course.objects.filter(pk__in=[i.course_id for i in user_courses]).count()
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
    context = {
        "user": user,
        "courses": courses
    }
    return render(request, 'index.html', context)
