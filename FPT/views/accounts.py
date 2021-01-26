from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserForm, TraineeForm, TrainerForm
from FPT.models import Trainer, Trainee, User

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def account_manage(request):
    if request.user.is_staff:
        users = User.objects.exclude(
            Q(is_staff=True) |
            Q(is_superuser=True)
        )
        context = {
            "users_info": users,
        }
        return render(request, "account_manage.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def manage_profile(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=int(user_id))
        except User.DoesNotExist:
            messages.error(request, "Not found User in system")
            return redirect('FPT:account-manage')

        if user.is_staff or user.is_superuser:
            messages.warning(request, "You don't have permission to action")
            return redirect("FPT:account-manage")

        context = {
            "user_info": user,
        }
        try:
            if user.is_trainer:
                trainer = Trainer.objects.get(pk=user.id)
                context["user_type"] = trainer
            elif user.is_trainee:
                trainee = Trainee.objects.get(pk=user.id)
                context["user_type"] = trainee
            else:
                context["user_type"] = None
        except Trainee.DoesNotExist or Trainer.DoesNotExist:
            messages.error(request, "Can not find info user ")
            return redirect("FPT:account-manage")

        return render(request, 'manage-profile.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def change_profile_user(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.success(request, "Not found User in system")
            return redirect("FPT:account-manage")
        if request.method == 'POST':
            user_change = UserForm(request.POST, request.FILES, instance=user)
            if user_change.is_valid():
                user_change.save()
                messages.success(request, "Update User info success")
                return redirect("FPT:manage-profile", user.id)
        if user.is_trainer:
            upload_form = TrainerForm()
        elif user.is_trainee:
            upload_form = TraineeForm()
        else:
            upload_form = None
        context = {
            "user_info": user,
            "upload_form": upload_form
        }
        return render(request, "registration/profile-update.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def reset_password(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.success(request, "Not found User in system")
            return redirect("FPT:account-manage")
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                user_change = form.save()
                update_session_auth_hash(request, user_change)  # Important!
                messages.success(request, 'User password was successfully reset')
                return redirect('FPT:manage-profile', user.id)
            else:
                messages.warning(request, 'Please correct the error below.')
                return redirect('FPT:manage-profile', user.id)
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/change_password.html', {
            'form': form,
            'type': 'reset',
            'user_info': user
        })
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def change_profile_trainer(request, user_id):
    if request.user.id == user_id or request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainer = Trainer.objects.get(pk=int(user_id))
        except User.DoesNotExist or Trainer.DoesNotExist:
            messages.success(request, "Not found Trainer in system")
            return redirect("FPT:dashboard")

        if user.is_superuser or user.is_staff or user.is_trainer:
            if request.method == 'POST':
                trainer_change = TrainerForm(request.POST, instance=trainer)
                if trainer_change.is_valid():
                    trainer_change.save()
                    if user.is_staff:
                        messages.success(request, 'Trainer info was successfully update')
                        return redirect("FPT:manage-profile", user.id)
                    if user.is_trainer:
                        messages.success(request, 'Your Trainer info was successfully update')
                        return redirect("FPT:profile")
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:dashboard")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def change_profile_trainee(request, user_id):
    if request.user.id == user_id or request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainee = Trainee.objects.get(pk=int(user_id))
        except User.DoesNotExist or Trainer.DoesNotExist:
            messages.success(request, "Not found Trainer in system")
            return redirect("FPT:dashboard")
        if user.is_superuser or user.is_staff or user.is_trainee:
            if request.method == 'POST':
                trainee_change = TraineeForm(request.POST, instance=trainee)
                if trainee_change.is_valid():
                    trainee_change.save()
                    if user.is_staff:
                        messages.success(request, 'Trainee info was successfully update')
                        return redirect("FPT:manage-profile", user.id)
                    if user.is_trainee:
                        messages.success(request, 'Your Trainee info was successfully update')
                        return redirect("FPT:profile")
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:dashboard")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def remove_user(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist or Trainer.DoesNotExist:
            messages.success(request, "Not found Trainer in system")
            return redirect("FPT:dashboard")
        if request.method == "POST":
            user.delete()
            return HttpResponse(status=204)
            # messages.success(request, "Delete course success")
            # return redirect("FPT:account-manage")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def search_users(request):
    if request.user.is_staff:
        if request.method == "POST":
            users = User.objects.filter(
                Q(full_name__icontains=request.POST["q"]) |
                Q(username__icontains=request.POST["q"]) |
                Q(email__icontains=request.POST["q"])
            )
            if users.count() > 0:
                messages.success(request, f"Search users success with {users.count()} results")
                context = {
                    "users_info": users
                }
                return render(request, "account_manage.html", context)

            messages.warning(request, f"Not found users {request.POST['q']}")
            context = {
                "users_info": users
            }
            return render(request, "account_manage.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
