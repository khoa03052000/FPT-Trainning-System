from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.forms import CourseCreate
from FPT.models import Course, Trainer, Trainee, AssignUserToCourse


@require_http_methods(["GET"])
@login_required
def manage_courses(request):
    if request.user.is_staff:
        user = request.user
        courses = Course.objects.all()
        context = {
            "user": user,
            "courses": courses,
        }
        return render(request, 'course.html', context=context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def create_course(request):
    if request.user.is_staff:
        upload = CourseCreate()
        if request.method == 'POST':
            check_course = Course.objects.get(name=request.POST["name"])
            if check_course:
                messages.warning(request, f"The course with name {check_course.name} is exist")
                return redirect('FPT:create-course')
            upload = CourseCreate(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                messages.success(request, "Create course success")
                return redirect('FPT:courses')
            else:
                messages.error(request, "Your form is not valid for create course")
                return redirect('FPT:courses')
        else:
            return render(request, 'course_create.html', {'upload_form': upload})
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def course_detail(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect("FPT:courses")

        assign_user = AssignUserToCourse.objects.filter(course__id=course_id)

        trainer_type = ContentType.objects.get_for_model(Trainer)
        trainee_type = ContentType.objects.get_for_model(Trainee)

        trainers = [
            u.assigned_user
            for u in assign_user
            if (u.assigned_user_type_id == trainer_type.id)
        ]
        trainees = [
            u.assigned_user
            for u in assign_user
            if (u.assigned_user_type_id == trainee_type.id)
        ]

        context = {
            "course": course,
            "trainers": trainers,
            "trainees": trainees,
        }
        count = len(trainees) + len(trainers)
        if count > 0:
            percent_trainer = (len(trainers) / count) * 100
            percent_trainee = (len(trainees) / count) * 100
            context["percent_trainer"] = percent_trainer
            context["percent_trainee"] = percent_trainee
        return render(request, 'course_details.html', context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def update_course(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course_self = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect("FPT:courses")
        if request.method == 'GET':
            course_form = CourseCreate()
            context = {
                'upload_form': course_form,
                'course': course_self
            }
            return render(request, 'course_update.html', context)
        if request.method == 'POST':
            check_course = Course.objects.get(name=request.POST["name"])
            if check_course:
                messages.warning(request, f"The course with name {check_course.name} is exist")
                return redirect("FPT:course-detail", course_id=course_self.id)
            course_form = CourseCreate(request.POST, request.FILES, instance=course_self)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, "Update course success")
                return redirect("FPT:course-detail", course_id=course_self.id)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST", "GET"])
@login_required
def delete_course(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course_self = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect('FPT:courses')
        course_self.delete()
        if request.method == "POST":
            return HttpResponse(status=204)
        messages.success(request, "Delete course success")
        return redirect("FPT:courses")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
def set_visible(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course_self = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect('FPT:courses')
        if course_self.is_visible:
            course_self.is_visible = False
            course_self.save()
            messages.success(request, "Set course is not visible success")
            return redirect("FPT:courses")
        course_self.is_visible = True
        course_self.save()
        messages.success(request, "Set course is visible success")
        return redirect("FPT:courses")
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def search_courses(request):
    if request.user.is_staff:
        if request.method == "POST":
            courses = Course.objects.filter(
                Q(name__icontains=request.POST["q"]) |
                Q(description__icontains=request.POST["q"])
            )
            if courses.exists():
                messages.success(request, f"Search courses success with {courses.count()} results")
                context = {"courses": courses}
                return render(request, "course.html", context)

            messages.warning(request, f"Not found category {request.POST['q']}")
            context = {
                "courses": courses
            }
            return render(request, "course.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
