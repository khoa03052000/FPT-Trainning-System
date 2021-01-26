from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserForm, TraineeForm, TrainerForm
from FPT.models import Trainer, Trainee

User = get_user_model()


@require_http_methods(["GET"])
@login_required
def get_profile(request):
    user = User.objects.get(pk=request.user.id)
    context = {
        "user": user,
    }
    if user.is_trainer:
        trainer = Trainer.objects.get(pk=user.id)
        context["user_type"] = trainer
    elif user.is_trainee:
        trainee = Trainee.objects.get(pk=user.id)
        context["user_type"] = trainee
    else:
        context["user_type"] = None

    return render(request, 'registration/profile.html', context)


@require_http_methods(["GET", "POST"])
@login_required
def change_profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        user_change = UserForm(request.POST, request.FILES, instance=user)
        if user_change.is_valid():
            user_change.save()
            return redirect("FPT:profile", user.id)
    if user.is_trainer:
        upload_form = TrainerForm()
    elif user.is_trainee:
        upload_form = TraineeForm()
    else:
        upload_form = None
    context = {
        "user": user,
        "upload_form": upload_form
    }
    return render(request, "registration/profile-update.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def change_password(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user_change = form.save()
            update_session_auth_hash(request, user_change)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('FPT:profile')
        else:
            messages.warning(request, 'Please correct the error below.')
            return redirect('FPT:profile')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
