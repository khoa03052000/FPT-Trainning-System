from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserForm, TraineeForm, TrainerForm, UserFPTCreationForm
from FPT.models import Trainer, Trainee


User = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def register_users(request):
    if request.user.is_staff:
        user_form = UserFPTCreationForm()
        if request.method == 'POST':
            user_create = UserFPTCreationForm(request.POST)
            if user_create.is_valid():
                user_create.save(commit=True)
                messages.success(request, "Create User Account successfully, Please fill User Infor")
                return redirect("FPT:account-manage")
            messages.error(request, "Can't create User and UserProfile without database save ")
            return redirect("FPT:account-manage")
        context = {"form": user_form}
        return render(request, 'registration/register.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
