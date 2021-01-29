from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserForm, TraineeForm, TrainerForm
from FPT.models import Trainer, Trainee

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def account_manage(request):
    if request.user.is_staff:
        users = User.objects.exclude(
            Q(is_staff=True) |
            Q(is_superuser=True) |
            Q(is_trainer=True) |
            Q(is_trainee=False)
        )
        trainees = Trainee.objects.filter(pk__in=[user.id for user in users])
        context = {
            "trainees": trainees,
        }
        return render(request, "account_manage.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@login_required
@require_http_methods(["GET"])
def account_manage_trainer(request):
    if request.user.is_staff:
        users = User.objects.exclude(
            Q(is_staff=True) |
            Q(is_superuser=True) |
            Q(is_trainee=True) |
            Q(is_trainer=False)
        )
        trainers = Trainer.objects.filter(pk__in=[user.id for user in users])
        context = {
            "trainers": trainers,
        }
        return render(request, "account_manage_trainer.html", context)
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

        context = {
            "user_info": user,
        }
        if user.is_trainer:
            try:
                trainer = Trainer.objects.get(pk=user.id)
                context["user_type"] = trainer
            except Trainer.DoesNotExist:
                context["user_type"] = None
        if user.is_trainee:
            try:
                trainee = Trainee.objects.get(pk=user.id)
                context["user_type"] = trainee
            except Trainee.DoesNotExist:
                context["user_type"] = None
        return render(request, 'manage-profile.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def add_trainer(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, "Not found User in system")
            return redirect("FPT:account-manage")
        if user.is_trainer:
            Trainer.objects.create(user=user)
            return redirect("FPT:change-profile-trainer", user.id)
        messages.warning(request, "User no is trainer")
        return redirect("FPT:manage-profile", user.id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def change_profile_user(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, "Not found User in system")
            return redirect("FPT:account-manage")
        if user.is_trainee:
            if request.method == 'POST':
                user_change = UserForm(request.POST, request.FILES, instance=user)
                if user_change.is_valid():
                    user_change.save()
                    messages.success(request, "Update User info success")
                    return redirect("FPT:manage-profile", user.id)
                messages.error(request, "Update User info error, try again")
                return redirect("FPT:manage-profile", user.id)
            else:
                upload_form = UserForm()
                try:
                    user_type = Trainee.objects.get(user=user)
                except Trainee.DoesNotExist:
                    messages.error(request, "Trainee info not found for update")
                    return redirect("FPT:manage-profile", user.id)
                context = {
                    "user_info": user,
                    "upload_form": upload_form,
                    "user_type": user_type
                }
                return render(request, "registration/user_info.html", context)
        messages.error(request, "User is not Trainee")
        return redirect("FPT:manage-profile", user.id)
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
        if user.is_trainee:
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
        messages.warning(request, "You don't have permission to reset password trainer")
        return redirect("FPT:manage-profile", user.id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST", "GET"])
@login_required
def change_profile_trainer(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainer = Trainer.objects.get(pk=user.id)
        except User.DoesNotExist or Trainer.DoesNotExist:
            messages.error(request, "Not found Trainer in system")
            return redirect("FPT:manage-profile", user_id)

        if user.is_trainer:
            if request.method == "POST":
                trainer_change = TrainerForm(request.POST, instance=trainer)
                if trainer_change.is_valid():
                    trainer_change.save()
                    messages.success(request, 'Trainer info was successfully update')
                    return redirect("FPT:manage-profile", user.id)
                messages.warning(request, "Please try again, error form")
                return redirect("FPT:manage-profile", user_id)
            trainer_change = TrainerForm()
            context = {
                "user_info": user,
                "upload_form": trainer_change,
                "user_type": trainer
            }
            return render(request, "registration/trainer_info.html", context)
        messages.warning(request, "User don't have permission to action")
        return redirect("FPT:manage-profile", user_id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST", "GET"])
@login_required
def change_profile_trainee(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainee = Trainee.objects.get(pk=user.id)
        except User.DoesNotExist or Trainee.DoesNotExist:
            messages.error(request, "Not found Trainer in system")
            return redirect("FPT:manage-profile", user_id)

        if user.is_trainee:
            if request.method == "POST":
                trainee_change = TraineeForm(request.POST, instance=trainee)
                if trainee_change.is_valid():
                    trainee_change.save()
                    messages.success(request, 'Trainee info was successfully update')
                    return redirect("FPT:manage-profile", user.id)
                messages.warning(request, "Please try again, error form")
                return redirect("FPT:manage-profile", user_id)
            trainee_change = TraineeForm()
            context = {
                "user_info": user,
                "upload_form": trainee_change,
                "user_type": trainee
            }
            return render(request, "registration/trainee_info.html", context)
        messages.warning(request, "User don't have permission to action")
        return redirect("FPT:dashboard")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def remove_user(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainee = Trainee.objects.get(user=user)
        except User.DoesNotExist or Trainee.DoesNotExist:
            messages.success(request, "Not found Trainee in system")
            return redirect("FPT:dashboard")
        if user.is_trainee:
            if request.method == "POST":
                user.delete()
                return HttpResponse(status=204)
                # messages.success(request, "Delete course success")
                # return redirect("FPT:account-manage")
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:dashboard")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def search_users(request):
    if request.user.is_staff:
        if request.method == "POST":
            trainees = Trainee.objects.filter(
                Q(user__full_name__icontains=request.POST["q"]) |
                Q(phone__icontains=request.POST["q"]) |
                Q(age__icontains=request.POST["q"]) |
                Q(dot__icontains=request.POST["q"]) |
                Q(education__icontains=request.POST["q"]) |
                Q(location__icontains=request.POST["q"]) |
                Q(experience__icontains=request.POST["q"])
            )
            if trainees.count() > 0:
                messages.success(request, f"Search users success with {trainees.count()} results")
                context = {
                    "trainees": trainees
                }
                return render(request, "account_manage.html", context)

            messages.warning(request, f"Not found users {request.POST['q']}")
            context = {
                "trainees": trainees
            }
            return render(request, "account_manage.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def remove_trainer(request, user_id):
    if request.user.is_staff:
        try:
            user = User.objects.get(pk=user_id)
            trainer = Trainer.objects.get(user=user)
        except User.DoesNotExist or Trainer.DoesNotExist:
            messages.success(request, "Not found Trainee in system")
            return redirect("FPT:dashboard")
        trainer.delete()
        messages.success(request, "Delete trainer info success")
        return redirect("FPT:manage-profile", user.id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
