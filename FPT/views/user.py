from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import UserForm, TraineeForm, TrainerForm
from FPT.models import Trainer, Trainee, AssignUserToCourse, Course, Request
from FPT_Trainning.tasks import send_notification

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
            messages.success(request, "User info update successfully")
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
        messages.error(request, "Not found Trainee in system")
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
        messages.error(request, "Not found Trainer in system")
        return redirect("FPT:dashboard")
    trainer_change = TrainerForm(request.POST, instance=trainer)
    if trainer_change.is_valid():
        trainer_change.save()
        messages.success(request, 'Your Trainer info was successfully update')
        return redirect("FPT:profile")
    else:
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:profile")


@require_http_methods(["GET"])
@login_required
def view_assigned_course(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.warning(request, "You don't have permission to action")
        return redirect("FPT:dashboard")
    else:
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            user = None
        if user:
            if user.is_trainee:
                trainee_type = ContentType.objects.get_for_model(Trainee)
                user_assigned = AssignUserToCourse.objects.filter(
                    assigned_user_type=trainee_type,
                    assigned_user_id=user.id
                )
                courses = Course.objects.filter(pk__in=[item.course_id for item in user_assigned])
                context = {
                    "user_assigned": user_assigned,
                    "courses": courses,
                }
            if user.is_trainer:
                trainer_type = ContentType.objects.get_for_model(Trainer)
                user_assigned = AssignUserToCourse.objects.filter(
                    assigned_user_type=trainer_type,
                    assigned_user_id=user.id
                )
                courses = Course.objects.filter(pk__in=[item.course_id for item in user_assigned])
                context = {
                    "user_assigned": user_assigned,
                    "courses": courses,
                }
            return render(request, "view_assigned_course.html", context)
        messages.error(request, "User Not Found")
        return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def view_course_assigned_detail(request, course_id):
    if request.user.is_staff:
        messages.warning(request, "You are Staff, please use view Course Details for Staff")
        return redirect("FPT:course-detail", course_id)
    else:
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Course Not Found")
            return redirect("FPT:view-assigned-course")
        context = {
            'course': course
        }
        return render(request, "view_assigned_course_details.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def request_assign_course(request, course_id):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        messages.error(request, "Not Found User")
        return redirect("login")
    if user.is_trainee:
        if request.method == "POST":
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                messages.error(request, "Not Found Course")
                return redirect("FPT:dashboard")
            email = request.POST['email']
            content = request.POST['content']
            check_request = Request.objects.filter(user=user, course=course)
            if check_request.count() > 3:
                messages.warning(request, "You have full request for course")
                return redirect('FPT:view-request-assign')
            else:
                request_assign = Request.objects.create(
                    email=email,
                    content=content,
                    user=user,
                    course=course
                )
                send_notification(request_assign)
            messages.success(request, "Please check email for notification")
            return redirect('FPT:view-request-assign')
        else:
            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                messages.error(request, "Not Found Course")
                return redirect("FPT:dashboard")
            context = {
                'course': course
            }
            return render(request, 'request_form.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def view_request_assign(request):
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        messages.error(request, "Not Found User")
        return redirect("login")
    if user.is_trainee:
        requests_assign = Request.objects.filter(user=user)
        context = {
            "requests_assign": requests_assign
        }
        return render(request, 'request_list.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")