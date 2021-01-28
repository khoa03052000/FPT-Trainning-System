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
        try:
            trainer = Trainer.objects.get(pk=user.id)
            context["user_type"] = trainer
        except Trainer.DoesNotExist:
            messages.error(request, "Not Found Info Trainer")
            return redirect("FPT:dashboard")
    elif user.is_trainee:
        try:
            trainee = Trainee.objects.get(pk=user.id)
            context["user_type"] = trainee
        except Trainee.DoesNotExist:
            messages.error(request, "Not Found Info Trainee")
            return redirect("FPT:dashboard")
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
            return redirect("FPT:profile")
    if user.is_trainer:
        upload_form = TrainerForm()
        try:
            user_type = Trainer.objects.get(user=user)
        except Trainer.DoesNotExist:
            messages.error(request, "Trainer info not found for update")
            return redirect("FPT:profile")
    elif user.is_trainee:
        upload_form = TraineeForm()
        try:
            user_type = Trainee.objects.get(user=user)
        except Trainee.DoesNotExist:
            messages.error(request, "Trainee info not found for update")
            return redirect("FPT:profile")
    else:
        upload_form = None
        user_type = None
    context = {
        "user": user,
        "upload_form": upload_form,
        "user_type": user_type
    }
    return render(request, "registration/profile-update.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def change_password(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
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


@require_http_methods(["POST"])
@login_required
def update_profile_trainee(request):
    try:
        user = User.objects.get(pk=request.user.id)
        trainee = Trainee.objects.get(pk=user.id)
    except User.DoesNotExist or Trainee.DoesNotExist:
        messages.success(request, "Not found Trainee in system")
        return redirect("FPT:dashboard")
    trainee_change = TraineeForm(request.POST, instance=trainee)
    if trainee_change.is_valid():
        trainee_change.save()
        messages.success(request, 'Your Trainee info was successfully update')
        return redirect("FPT:profile")
    else:
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:profile")


@require_http_methods(["POST"])
@login_required
def update_profile_trainer(request):
    try:
        user = User.objects.get(pk=request.user.id)
        trainer = Trainer.objects.get(pk=user.id)
    except User.DoesNotExist or Trainee.DoesNotExist:
        messages.success(request, "Not found Trainer in system")
        return redirect("FPT:dashboard")
    trainer_change = TrainerForm(request.POST, instance=trainer)
    if trainer_change.is_valid():
        trainer_change.save()
        messages.success(request, 'Your Trainer info was successfully update')
        return redirect("FPT:profile")
    else:
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:profile")