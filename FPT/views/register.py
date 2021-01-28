from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserFPTCreationForm

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
                context = {
                    'user_type': user_create.instance.trainee,
                    'user_info': user_create.instance
                }
                messages.success(request, "Create Trainee successfully, Please fill Trainee Info")
                return render(request, 'registration/new_trainee_info.html', context)
            messages.error(request, "Can't create Trainee and Trainee Profile without database save ")
            return redirect("FPT:register-users")
        context = {"form": user_form}
        return render(request, 'registration/register.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
