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
    path('create-course/', views.create_course, name='create-course'),
    path('course-detail/<int:course_id>/', views.course_detail, name='course-detail'),

    # Category
    path('categories/', views.manage_categories, name='categories'),
    path('create-categories/', views.create_category, name='create_category'),
    path('categories/detail/<int:category_id>/', views.category_detail, name='category-detail'),
    path('update-category/<int:category_id>/', views.update_category, name='update_category'),

    path('register/', views.get_dashboard, name='register'),
    path('account-manage/', views.get_dashboard, name='account-manage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
