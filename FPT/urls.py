from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'FPT'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.get_profile, name='profile'),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    # Course
    path('courses/', views.manage_courses, name='courses'),
    path('courses/create-course/', views.create_course, name='create-course'),
    path('courses/course-detail/<int:course_id>/', views.course_detail, name='course-detail'),
    path('courses/update-course/<int:course_id>/', views.update_course, name='update-course'),
    path('courses/delete-course/<int:course_id>/', views.delete_course, name='delete-course'),
    path('courses/assign-course/<int:course_id>/', views.assign_course, name='assign-course'),
    # Category
    path('categories/', views.manage_categories, name='categories'),
    path('categories/create-category/', views.create_category, name='create-category'),
    path('categories/category-detail/<int:category_id>/', views.category_detail, name='category-detail'),
    path('categories/update-category/<int:category_id>/', views.update_category, name='update-category'),
    # path('categories/delete-category/<int:category_id>/', views.delete_category, name='delete-category'),
    # User
    path('register/', views.get_dashboard, name='register'),
    path('account-manage/', views.get_dashboard, name='account-manage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
