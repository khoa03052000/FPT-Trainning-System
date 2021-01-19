from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'FPT'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.get_profile, name='profile'),
    path('dashboard/', views.get_dashboard, name='dashboard'),
    path('courses/', views.get_dashboard, name='courses'),
    path('categories/', views.get_dashboard, name='categories'),
    path('register/', views.get_dashboard, name='register'),
    path('account-manage/', views.get_dashboard, name='account-manage'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
