from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.models import Request, AssignUserToCourse
from FPT_Trainning.tasks import send_notification_user

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def requests_users(request):
    if request.user.is_staff:
        requests_assign = Request.objects.all()
        context = {
            'requests_assign': requests_assign
        }
        return render(request, 'request_list.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@login_required
@require_http_methods(["GET"])
def approve_request(request, request_id):
    if request.user.is_staff:
        try:
            request_assign = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            messages.error(request, 'Not Found Request Assign')
            return redirect('FPT:requests-users')
        if request_assign.status == request_assign.APPROVED:
            messages.warning(request, 'The Request is APPROVED, can not use action')
            return redirect("FPT:requests-users")
        if request_assign.status == request_assign.PENDING:
            request_assign.status = request_assign.APPROVED
            request_assign.save()
            AssignUserToCourse.objects.get_or_create(
                assigned_user_id=request_assign.user_id,
                course=request_assign.course,
                assigned_user_type_id=8
            )
            send_notification_user(request_assign, "Approved Request Successfully, Please join Course for learn")
            messages.success(request, 'Approved Request Successfully, system send email notification for user')
            return redirect("FPT:requests-users")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@login_required
@require_http_methods(["GET"])
def reject_request(request, request_id):
    if request.user.is_staff:
        try:
            request_assign = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            messages.error(request, 'Not Found Request Assign')
            return redirect('FPT:requests-users')
        if request_assign.status == request_assign.APPROVED:
            messages.warning(request, 'The Request is APPROVED, can not use action')
            return redirect("FPT:requests-users")
        if request_assign.status == request_assign.PENDING:
            request_assign.status = request_assign.REJECTED
            request_assign.save()
            send_notification_user(request_assign, "REJECTED Request Successfully")
            messages.success(request, 'REJECTED Request Successfully, system send email notification for user')
            return redirect("FPT:requests-users")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@login_required
@require_http_methods(["GET"])
def remove_request(request, request_id):
    if request.user.is_staff:
        try:
            request_assign = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            messages.error(request, 'Not Found Request Assign')
            return redirect('FPT:requests-users')

        if request_assign.status == request_assign.APPROVED:
            messages.warning(request, 'The Request is APPROVED, can not use action')
            return redirect("FPT:requests-users")

        if request_assign.status == request_assign.PENDING or request_assign.status == request_assign.REJECTED:
            request_assign.status = request_assign.CANCELLED
            request_assign.save()
            send_notification_user(request_assign, "CANCELLED Request Successfully")
            messages.success(request, 'CANCELLED Request Successfully, system send email notification for user')
            return redirect("FPT:requests-users")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
