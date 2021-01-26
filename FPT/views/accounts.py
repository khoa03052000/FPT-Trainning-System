from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods

from FPT.forms import CourseCreate, CategoryCreate, UserForm, TraineeForm, TrainerForm
from FPT.models import Course, Trainer, Trainee, User, Request, Category, AssignUserToCourse
from django.http import HttpResponse, response, HttpResponseNotFound
from django.views.generic import ListView
from django.db.models import Q

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def account_manage(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "account_manage.html", context)


@require_http_methods(["GET"])
@login_required
def manage_profile(request, user_id):
    user = User.objects.get(pk=int(user_id))
    context = {
        "user": user
    }
    return render(request, 'registration/profile.html', context)


@require_http_methods(["POST"])
@login_required
def change_profile_trainer(request, user_id):
    trainer = Trainer.objects.get(pk=int(user_id))
    user = User.objects.get(pk=request.user.id)
    if user.is_superuser or user.is_staff or user.is_trainee:
        if request.method == 'POST':
            trainer_change = TrainerForm(request.POST, request.FILES, instance=trainer)
            if trainer_change.is_valid():
                trainer_change.save()
                return redirect("FPT:profile", user.id)
    return HttpResponseNotFound('<h1>Page not found</h1>')


@require_http_methods(["GET", "POST"])
@login_required
def change_profile_trainee(request, user_id):
    user = User.objects.get(pk=int(user_id))
    if request.method == 'POST':
        user_change = UserForm(request.POST, request.FILES, instance=user)
        if user_change.is_valid():
            user_change.save()
            return redirect("FPT:profile", user.id)
    return render(request, "registration/profile-update.html", context={"user": user})