from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('role-select/', views.role_select, name='role_select'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/instructor/', views.instructor_register, name='instructor_register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('instructor/students/', views.instructor_students, name='instructor_students'),
    path('instructor/grade/edit/<int:grade_id>/', views.grade_edit, name='grade_edit'),
    path('instructor/profile/edit/', views.instructor_profile_edit, name='instructor_profile_edit'),
    path('student/edit/', views.student_edit, name='student_edit'),
    path('student/enroll/', views.student_enroll, name='student_enroll'),
    path('student/pay/', views.student_payment, name='student_payment'),
]