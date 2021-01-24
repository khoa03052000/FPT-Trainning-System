from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_http_methods

from .forms import CourseCreate, CategoryCreate, AssignCourseCreate
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


# Manage Course
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

    trainers = [
        u.assigned_user
        for u in assign_user
        if(u.assigned_user_type_id == trainer_type.id)
    ]
    trainees = [
        u.assigned_user
        for u in assign_user
        if(u.assigned_user_type_id == trainee_type.id)
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

    trainers = [
        u.assigned_user
        for u in assign_user
        if(u.assigned_user_type_id == trainer_type.id)
    ]
    trainees = [
        u.assigned_user
        for u in assign_user
        if(u.assigned_user_type_id == trainee_type.id)
    ]

    context = {
        "course": course,
        "trainers": trainers,
        "trainees": trainees
    }
    return render(request, "assign.html", context)


# Add Assign Trainer
@require_http_methods(["GET", "POST"])
def add_trainers_assign(request, course_id):
    course_id = int(course_id)
    try:
        course_self = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('FPT:courses')
    # Get info Course Assign and Type User
    trainer_type = ContentType.objects.get_for_model(Trainer)
    course_assign = AssignUserToCourse.objects.filter(course=course_self, assigned_user_type=trainer_type)

    # Check Trainer assigned in Course
    list_trainer_id_assigned = [i.assigned_user_id for i in course_assign]
    if len(list_trainer_id_assigned) > 3:
        return redirect('FPT:assign-course', course_id=course_id)

    # Handler Create List Trainers
    if request.method == "POST":

        trainers_id_list = request.POST.getlist('list-trainers')
        for i in range(0, len(trainers_id_list)):
            trainers_id_list[i] = int(trainers_id_list[i])

        check_trainers_id_list = [trainer_id for trainer_id in trainers_id_list if (trainer_id not in list_trainer_id_assigned)]

        list_assign_trainers = [
            AssignUserToCourse(
                assigned_user_id=int(trainer_id),
                course=course_self,
                assigned_user_type=trainer_type
            )
            for trainer_id in check_trainers_id_list
        ]
        AssignUserToCourse.objects.bulk_create(list_assign_trainers)
        return redirect('FPT:assign-course', course_id=course_id)

    trainers = Trainer.objects.exclude(pk__in=list_trainer_id_assigned)
    context = {
        "trainers": trainers,
        "course": course_self
    }
    return render(request, "assign-trainer.html", context)


@require_http_methods(["POST"])
def remove_assign_trainer(request, course_id, trainer_id):
    trainer_id = int(trainer_id)
    course_id = int(course_id)
    try:
        course_assign = AssignUserToCourse.objects.get(
            course__id=course_id,
            assigned_user_id=trainer_id
        )
    except AssignUserToCourse.DoesNotExist:
        return redirect('FPT:assign-course')
    course_assign.delete()
    return HttpResponse(status=204)


# Add Trainee Assign
@require_http_methods(["GET", "POST"])
def add_trainees_assign(request, course_id):
    course_id = int(course_id)
    try:
        course_self = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return redirect('FPT:courses')
    # Get info Course Assign and Type User
    trainee_type = ContentType.objects.get_for_model(Trainee)
    course_assign = AssignUserToCourse.objects.filter(course=course_self, assigned_user_type=trainee_type)

    # Check Trainee assigned in Course
    list_trainee_id_assigned = [i.assigned_user_id for i in course_assign]

    trainees = Trainee.objects.exclude(pk__in=list_trainee_id_assigned)
    # Handler Create List Trainees
    if request.method == "POST":

        trainees_id_list = request.POST.getlist('list-trainees')
        for i in range(0, len(trainees_id_list)):
            trainees_id_list[i] = int(trainees_id_list[i])

        check_trainee_id_list = [trainee_id for trainee_id in trainees_id_list if (trainee_id not in list_trainee_id_assigned)]

        list_assign_trainees = [
            AssignUserToCourse(
                assigned_user_id=trainee_id,
                course=course_self,
                assigned_user_type=trainee_type
            )
            for trainee_id in check_trainee_id_list
        ]
        AssignUserToCourse.objects.bulk_create(list_assign_trainees)
        return redirect('FPT:assign-course', course_id=course_id)
    context = {
        "trainees": trainees,
        "course": course_self
    }
    return render(request, "assign-trainee.html", context)


@require_http_methods(["POST"])
def remove_assign_trainee(request, course_id, trainee_id):
    trainee_id = int(trainee_id)
    course_id = int(course_id)
    try:
        course_assign = AssignUserToCourse.objects.get(
            course__id=course_id,
            assigned_user_id=trainee_id
        )
    except AssignUserToCourse.DoesNotExist:
        return redirect('FPT:assign-course')
    course_assign.delete()
    return HttpResponse(status=204)


@require_http_methods(["GET"])
def manage_assign(request):
    trainer_type = ContentType.objects.get_for_model(Trainer)
    trainee_type = ContentType.objects.get_for_model(Trainee)

    trainers_assigned = AssignUserToCourse.objects.filter(assigned_user_type=trainer_type)
    trainees_assigned = AssignUserToCourse.objects.filter(assigned_user_type=trainee_type)
    
    list_trainers_id = [i.assigned_user_id for i in trainers_assigned]
    list_trainees_id = [i.assigned_user_id for i in trainees_assigned]

    trainers = Trainer.objects.filter(pk__in=list_trainers_id)
    trainees = Trainee.objects.filter(pk__in=list_trainees_id)

    context = {
        "trainers": trainers,
        "trainees": trainees,
    }
    return render(request, "manage-assign-user.html", context)


@require_http_methods(["GET", "POST"])
def change_trainer_assign(request, trainer_id):
    trainer_id = int(trainer_id)
    trainer = Trainer.objects.get(pk=trainer_id)
    trainer_in_course = AssignUserToCourse.objects.filter(
        assigned_user_id=trainer_id,
    )

    courses_id = [item.course_id for item in trainer_in_course]
    courses = Course.objects.filter(pk__in=courses_id)
    courses_upload = Course.objects.exclude(pk__in=courses_id)

    if request.method == "POST":
        course_upload_id = int(request.POST["course-upload"])
        course_change_id = int(request.POST["course_change_id"])

        for item in trainer_in_course:
            if item.course_id == course_change_id:
                item.course_id = course_upload_id
                item.save()
        return redirect("FPT:change-trainer-assign", trainer_id=trainer_id)
    context = {
        "trainer": trainer,
        "courses_upload": courses_upload,
        "courses": courses
    }
    return render(request, "change-assign-trainer.html", context)


@require_http_methods(["GET", "POST"])
def change_trainee_assign(request, trainee_id):
    trainee_id = int(trainee_id)
    trainee = Trainee.objects.get(pk=trainee_id)
    trainee_in_course = AssignUserToCourse.objects.filter(
        assigned_user_id=trainee_id,
    )

    courses_id = [item.course_id for item in trainee_in_course]
    courses = Course.objects.filter(pk__in=courses_id)
    courses_upload = Course.objects.exclude(pk__in=courses_id)

    if request.method == "POST":
        course_upload_id = int(request.POST["course-upload"])
        course_change_id = int(request.POST["course_change_id"])

        for item in trainee_in_course:
            if item.course_id == course_change_id:
                item.course_id = course_upload_id
                item.save()
        return redirect("FPT:change-trainee-assign", trainee_id=trainee_id)
    context = {
        "trainee": trainee,
        "courses_upload": courses_upload,
        "courses": courses
    }
    return render(request, "change-assign-trainee.html", context)


# Manage Categories
@require_http_methods(["GET"])
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


@require_http_methods(["GET", "POST"])
def delete_category(request, category_id):
    category_id = int(category_id)
    try:
        category_self = Category.objects.get(id=category_id)
    except Course.DoesNotExist:
        return redirect('FPT:categories')
    category_self.delete()
    if request.method == "POST":
        return HttpResponse(status=204)
    return redirect("FPT:categories")
