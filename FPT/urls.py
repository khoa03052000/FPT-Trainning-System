from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.courses import *
from .views.home import *
from .views.assign import *
from .views.accounts import *
from .views.categories import *
from .views.register import *
from .views.user import *


app_name = 'FPT'
urlpatterns = [
    # Index

    path('', index, name='index'),
    path('dashboard/', get_dashboard, name='dashboard'),
    # Course - Staff

    path('courses/', manage_courses, name='courses'),
    path('courses/create-course/', create_course, name='create-course'),
    path('courses/course-detail/<int:course_id>/', course_detail, name='course-detail'),
    path('courses/update-course/<int:course_id>/', update_course, name='update-course'),
    path('courses/delete-course/<int:course_id>/', delete_course, name='delete-course'),
    path('courses/set-visible/<int:course_id>/', set_visible, name='set-visible'),
    path('search-courses/', search_courses, name='search-courses'),
    # Assign Course - Staff

    path('courses/assign-course/<int:course_id>/', assign_course, name='assign-course'),
    # Manage Assign
    path('manage-assign/', manage_assign, name='manage-assign-user'),
    path('manage-assign/change-trainers/<int:trainer_id>', change_trainer_assign, name='change-trainer-assign'),
    path('manage-assign/change-trainees/<int:trainee_id>', change_trainee_assign, name='change-trainee-assign'),
    # Trainer Assign - Staff

    path('courses/assign-course/<int:course_id>/add-trainers/', add_trainers_assign, name='add-trainers-assign'),
    path('courses/assign-course/<int:course_id>/remove-trainers/<int:trainer_id>/', remove_assign_trainer, name='remove-assign-trainer'),

    # Trainee Assign - Staff

    path('courses/assign-course/<int:course_id>/add-trainees/', add_trainees_assign, name='add-trainees-assign'),
    path('courses/assign-course/<int:course_id>/remove-trainees/<int:trainee_id>/', remove_assign_trainee, name='remove-assign-trainee'),

    # Category - Staff
    path('categories/', manage_categories, name='categories'),
    path('search-categories/', search_category, name='search-categories'),
    path('categories/create-category/', create_category, name='create-category'),
    path('categories/category-detail/<int:category_id>/', category_detail, name='category-detail'),
    path('categories/update-category/<int:category_id>/', update_category, name='update-category'),
    path('categories/delete-category/<int:category_id>/', delete_category, name='delete-category'),

    # User - Manage - Staff
    path('register/', get_dashboard, name='register'),
    path('account-manage/', account_manage, name='account-manage'),
    path('manage-profile/<int:user_id>/', manage_profile, name='manage-profile'),
    path('change-profile-user/<int:user_id>/', change_profile_user, name='change-profile-user'),
    path('change-profile-trainer/<int:user_id>/', change_profile_trainer, name='change-profile-trainer'),
    path('change-profile-trainee/<int:user_id>/', change_profile_trainee, name='change-profile-trainee'),
    path('reset-password/<int:user_id>/', reset_password, name='reset-password'),
    path('remove-user/<int:user_id>/', remove_user, name='remove-user'),
    path('search-users/', search_users, name='search-users'),
    path('register-users/', register_users, name='register-users'),
    # User
    path('change-password/', change_password, name='change-password'),
    path('profile/', get_profile, name='profile'),
    path('change-profile/', change_profile, name='change-profile'),
    # TODO: VIEW COURSE ASSIGN
    # TODO; REQUEST COURSE
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
