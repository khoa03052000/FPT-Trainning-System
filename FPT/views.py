from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods

from .forms import CourseCreate, CategoryCreate
from .models import Course, Trainer, Trainee, User, Request, Category, AssignUserToCourse
from django.http import HttpResponse, response
from django.views.generic import ListView
from django.db.models import Q


# Create your views here.
def index(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def get_profile(request):
    return render(request, 'registration/profile.html')


@require_http_methods(["GET"])
def get_dashboard(request):
    user = request.user
    trainers = Trainer.objects.all().count()
    trainees = Trainee.objects.all().count()
    users = User.objects.filter(is_staff=True).count()
    requests = Request.objects.all().count()
    courses = Course.objects.all().count()
    context = {
        'trainers': trainers,
        'trainees': trainees,
        'users': users,
        'requests': requests,
        "user": user,
        "courses": courses
    }
    return render(request, 'index.html', context=context)


@require_http_methods(["GET"])
def manage_courses(request):
    user = request.user
    courses = Course.objects.all()
    context = {
        "user": user,
        "courses": courses,
    }
    return render(request, 'course.html', context=context)


@require_http_methods(["GET", "POST"])
def create_course(request):
    upload = CourseCreate()
    if request.method == 'POST':
        upload = CourseCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('FPT:courses')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'course_create.html', {'upload_form': upload})


@require_http_methods(["GET"])
def course_detail(request, course_id):
    course_id = int(course_id)
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect("FPT:courses")

    assign_user = AssignUserToCourse.objects.filter(course__id=course_id)
    
    trainer_type = ContentType.objects.get_for_model(Trainer)
    trainee_type = ContentType.objects.get_for_model(Trainee)

    trainers = []
    trainees = []

    for user in assign_user:
        if user.assigned_user_type.id == trainer_type.id:
            trainers.append(user.assigned_user)
        if user.assigned_user_type.id == trainee_type.id:
            trainees.append(user.assigned_user)

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


@require_http_methods(["GET", "POST"])
def update_course(request, course_id):
    course_id = int(course_id)
    try:
        course_self = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect("FPT:courses")
    if request.method == 'GET':
        course_form = CourseCreate()
        context = {
            'upload_form': course_form,
            'course': course_self
        }
        return render(request, 'course_update.html', context)
    if request.method == 'POST':
        course_form = CourseCreate(request.POST, request.FILES, instance=course_self)
        if course_form.is_valid():
            course_form.save()
            return redirect("FPT:course-detail", course_id=course_self.id)


@require_http_methods(["POST", "GET"])
def delete_course(request, course_id):
    course_id = int(course_id)
    try:
        course_self = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('FPT:courses')
    course_self.delete()
    if request.method == "POST":
        return HttpResponse(status=204)
    return redirect("FPT:courses")


@require_http_methods(["GET"])
def assign_course(request, course_id):
    course_id = int(course_id)
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect("FPT:courses")

    assign_user = AssignUserToCourse.objects.filter(course__id=course_id)

    trainer_type = ContentType.objects.get_for_model(Trainer)
    trainee_type = ContentType.objects.get_for_model(Trainee)

    trainers = []
    trainees = []

    for user in assign_user:
        if user.assigned_user_type.id == trainer_type.id:
            trainers.append(user.assigned_user)
        if user.assigned_user_type.id == trainee_type.id:
            trainees.append(user.assigned_user)
    context = {
        "course": course,
        "trainers": trainers,
        "trainees": trainees
    }
    return render(request, "assign.html", context)


@require_http_methods(["GET", "PUT", "DELETE"])
def manage_categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "category.html", context)


@require_http_methods(["GET", "POST"])
def create_category(request):
    upload = CategoryCreate()
    if request.method == 'POST':
        upload = CategoryCreate(request.POST)
        if upload.is_valid():
            upload.save()
            return redirect('FPT:categories')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'category_create.html', {'upload_form': upload})


@require_http_methods(["GET", "PUT"])
def category_detail(request, category_id):
    category_id = int(category_id)
    try:
        category_self = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return redirect("FPT:categories")
    context ={
        "category": category_self
    }
    return render(request, 'category_detail.html', context)


@require_http_methods(["GET", "POST"])
def update_category(request, category_id):
    category_id = int(category_id)
    try:
        category_self = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return redirect("FPT:category-detail")
    if request.method == 'GET':
        category_form = CategoryCreate()
        context = {
            'upload_form': category_form,
            'category': category_self
        }
        return render(request, 'category_update.html', context)
    if request.method == 'POST':
        category_form = CategoryCreate(request.POST, instance=category_self)
        if category_form.is_valid():
            category_form.save()
            return redirect("FPT:category-detail", category_id=category_self.id)