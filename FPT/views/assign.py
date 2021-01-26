from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from FPT.models import Course, Trainer, Trainee, AssignUserToCourse


@require_http_methods(["GET"])
@login_required
def assign_course(request, course_id):
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
            "trainees": trainees
        }
        return render(request, "assign.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


# Add Assign Trainer
@require_http_methods(["GET", "POST"])
@login_required
def add_trainers_assign(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course_self = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect("FPT:courses")
        # Get info Course Assign and Type User
        trainer_type = ContentType.objects.get_for_model(Trainer)
        course_assign = AssignUserToCourse.objects.filter(course=course_self, assigned_user_type=trainer_type)

        # Check Trainer assigned in Course
        list_trainer_id_assigned = [i.assigned_user_id for i in course_assign]
        if len(list_trainer_id_assigned) >= 3:
            messages.warning(request, "The course have full trainer!")
            return redirect('FPT:assign-course', course_id=course_id)

        # Handler Create List Trainers
        if request.method == "POST":
            trainers_id_list = request.POST.getlist('list-trainers')
            if len(trainers_id_list) > 3:
                messages.warning(request, "The course have full trainer!")
                return redirect('FPT:add-trainers-assign', course_id=course_id)
            for i in range(0, len(trainers_id_list)):
                trainers_id_list[i] = int(trainers_id_list[i])

            check_trainers_id_list = [trainer_id for trainer_id in trainers_id_list if
                                      (trainer_id not in list_trainer_id_assigned)]

            list_assign_trainers = [
                AssignUserToCourse(
                    assigned_user_id=int(trainer_id),
                    course=course_self,
                    assigned_user_type=trainer_type
                )
                for trainer_id in check_trainers_id_list
            ]
            AssignUserToCourse.objects.bulk_create(list_assign_trainers)
            messages.success(request, f"Successfully assigned {len(list_assign_trainers)} trainers to the course")
            return redirect('FPT:assign-course', course_id=course_id)

        trainers = Trainer.objects.exclude(pk__in=list_trainer_id_assigned)
        context = {
            "trainers": trainers,
            "course": course_self
        }
        return render(request, "assign-trainer.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def remove_assign_trainer(request, course_id, trainer_id):
    if request.user.is_staff:
        trainer_id = int(trainer_id)
        course_id = int(course_id)
        try:
            course_assign = AssignUserToCourse.objects.get(
                course__id=course_id,
                assigned_user_id=trainer_id
            )
        except AssignUserToCourse.DoesNotExist:
            messages.error(request, "Not found trainer in course")
            return redirect('FPT:assign-course')
        course_assign.delete()
        return HttpResponse(status=204)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


# Add Trainee Assign
@require_http_methods(["GET", "POST"])
@login_required
def add_trainees_assign(request, course_id):
    if request.user.is_staff:
        course_id = int(course_id)
        try:
            course_self = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Not found course")
            return redirect("FPT:courses")

        # Get info Course Assign and Type User
        trainee_type = ContentType.objects.get_for_model(Trainee)
        course_assign = AssignUserToCourse.objects.filter(course=course_self, assigned_user_type=trainee_type)

        # Check Trainee assigned in Course
        list_trainee_id_assigned = [i.assigned_user_id for i in course_assign]
        if len(list_trainee_id_assigned) >= 20:
            messages.warning(request, "The course have full trainee")
            return redirect('FPT:assign-course', course_id=course_id)

        # Handler Create List Trainees
        if request.method == "POST":
            trainees_id_list = request.POST.getlist('list-trainees')
            if len(trainees_id_list) > 20:
                messages.warning(request, "The course have full trainee!")
                return redirect('FPT:add-trainees-assign', course_id=course_id)

            for i in range(0, len(trainees_id_list)):
                trainees_id_list[i] = int(trainees_id_list[i])

            check_trainee_id_list = [trainee_id for trainee_id in trainees_id_list if
                                     (trainee_id not in list_trainee_id_assigned)]

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

        trainees = Trainee.objects.exclude(pk__in=list_trainee_id_assigned)
        context = {
            "trainees": trainees,
            "course": course_self
        }
        return render(request, "assign-trainee.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["POST"])
@login_required
def remove_assign_trainee(request, course_id, trainee_id):
    if request.user.is_staff:
        trainee_id = int(trainee_id)
        course_id = int(course_id)
        try:
            course_assign = AssignUserToCourse.objects.get(
                course__id=course_id,
                assigned_user_id=trainee_id
            )
        except AssignUserToCourse.DoesNotExist:
            messages.error(request, "Not found trainer in course")
            return redirect('FPT:assign-course')
        course_assign.delete()
        return HttpResponse(status=204)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET"])
@login_required
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
@login_required
def change_trainer_assign(request, trainer_id):
    if request.user.is_staff:
        trainer_id = int(trainer_id)
        try:
            trainer = Trainer.objects.get(pk=trainer_id)
        except Trainer.DoesNotExist:
            messages.error(request, "Not found trainer in course")
            return redirect('FPT:manage-assign-user')

        trainer_in_course = AssignUserToCourse.objects.filter(
            assigned_user_id=trainer_id,
        )
        if trainer_in_course.count() == 0:
            messages.warning(request, "Trainer is not assigned in course")
            return redirect('FPT:manage-assign-user')

        courses_id = [item.course_id for item in trainer_in_course]
        courses = Course.objects.filter(pk__in=courses_id)
        courses_upload = Course.objects.exclude(pk__in=courses_id)

        if request.method == "POST":
            course_upload_id = int(request.POST["course-upload"])
            if course_upload_id == 0:
                messages.error(request, f"No selected course, please choose one")
                return redirect("FPT:change-trainer-assign", trainer_id=trainer_id)

            course_change_id = int(request.POST["course_change_id"])

            for item in trainer_in_course:
                if item.course_id == course_change_id:
                    item.course_id = course_upload_id
                    item.save()
            course_change = Course.objects.get(id=course_upload_id).name
            messages.success(request, f"Trainer has been moved to the {course_change} course")
            return redirect("FPT:change-trainer-assign", trainer_id=trainer_id)
        context = {
            "trainer": trainer,
            "courses_upload": courses_upload,
            "courses": courses
        }
        return render(request, "change-assign-trainer.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")


@require_http_methods(["GET", "POST"])
@login_required
def change_trainee_assign(request, trainee_id):
    if request.user.is_staff:
        trainee_id = int(trainee_id)
        try:
            trainee = Trainee.objects.get(pk=trainee_id)
        except Trainee.DoesNotExist:
            messages.error(request, "Not found trainee in course")
            return redirect('FPT:manage-assign-user')

        trainee_in_course = AssignUserToCourse.objects.filter(
            assigned_user_id=trainee_id,
        )
        if trainee_in_course.count() == 0:
            messages.warning(request, "Trainee is not assigned in course")
            return redirect('FPT:manage-assign-user')

        courses_id = [item.course_id for item in trainee_in_course]
        courses = Course.objects.filter(pk__in=courses_id)
        courses_upload = Course.objects.exclude(pk__in=courses_id)

        if request.method == "POST":
            course_upload_id = int(request.POST["course-upload"])
            if course_upload_id == 0:
                messages.error(request, f"No selected course, please choose one")
                return redirect("FPT:change-trainee-assign", trainee_id=trainee_id)
            course_change_id = int(request.POST["course_change_id"])

            for item in trainee_in_course:
                if item.course_id == course_change_id:
                    item.course_id = course_upload_id
                    item.save()
            course_change = Course.objects.get(id=course_upload_id).name
            messages.success(request, f"Trainee has been moved to the {course_change} course")
            return redirect("FPT:change-trainee-assign", trainee_id=trainee_id)
        context = {
            "trainee": trainee,
            "courses_upload": courses_upload,
            "courses": courses
        }
        return render(request, "change-assign-trainee.html", context)
    messages.warning(request, "You don't have permission to action")
    return redirect("FPT:dashboard")
