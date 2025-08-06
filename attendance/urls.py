from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.teacher_login, name='teacher_login'),
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.teacher_logout, name='teacher_logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Attendance (register-style)
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),

    # Holiday Management
    path('holidays/', views.holiday_management, name='holiday_management'),
    path('holidays/<int:pk>/delete/', views.delete_holiday, name='delete_holiday'),

    # API endpoints
    path('api/student/<str:student_id>/attendance/', views.get_student_attendance_data, name='student_attendance_data'),
]
