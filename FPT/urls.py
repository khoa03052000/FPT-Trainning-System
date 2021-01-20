from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'FPT'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.get_profile, name='profile'),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    path('courses/', views.manage_courses, name='courses'),
    path('create-course/', views.create_course, name='create-course'),
    path('course-detail/<int:course_id>/', views.course_detail, name='course-detail'),
    path('categories/', views.get_dashboard, name='categories'),
    path('register/', views.get_dashboard, name='register'),
    path('account-manage/', views.get_dashboard, name='account-manage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
