#!/usr/bin/env python3
"""
Django Student Attendance Management System Setup Script
This script automatically sets up the project with sample data
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_attendance.settings')
    django.setup()

def create_superuser():
    """Create a superuser for admin access"""
    from django.contrib.auth.models import User

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superuser created (username: admin, password: admin123)")
    else:
        print("• Superuser 'admin' already exists")

def create_teacher():
    """Create a teacher user with teacher profile"""
    from django.contrib.auth.models import User
    from attendance.models import Teacher

    if not User.objects.filter(username='teacher').exists():
        user = User.objects.create_user('teacher', 'teacher@example.com', 'password123')
        teacher = Teacher.objects.create(
            user=user,
            name='Prof. Sarah Wilson',
            subject='Computer Science',
            phone='+1234567890'
        )
        print("✓ Teacher user created (username: teacher, password: password123)")
    else:
        print("• Teacher user 'teacher' already exists")

def create_sample_students():
    """Create sample students"""
    from attendance.models import Student

    students_data = [
        {
            'student_id': 'ST001',
            'name': 'John Doe',
            'email': 'john.doe@student.edu',
            'phone': '+1234567891',
            'address': '123 Main St, City, State 12345'
        },
        {
            'student_id': 'ST002',
            'name': 'Jane Smith',
            'email': 'jane.smith@student.edu',
            'phone': '+1234567892',
            'address': '456 Oak Ave, City, State 12345'
        },
        {
            'student_id': 'ST003',
            'name': 'Mike Johnson',
            'email': 'mike.johnson@student.edu',
            'phone': '+1234567893',
            'address': '789 Pine Rd, City, State 12345'
        },
        {
            'student_id': 'ST004',
            'name': 'Emily Davis',
            'email': 'emily.davis@student.edu',
            'phone': '+1234567894',
            'address': '321 Elm St, City, State 12345'
        },
        {
            'student_id': 'ST005',
            'name': 'David Wilson',
            'email': 'david.wilson@student.edu',
            'phone': '+1234567895',
            'address': '654 Maple Dr, City, State 12345'
        }
    ]

    created = 0
    for student_data in students_data:
        if not Student.objects.filter(student_id=student_data['student_id']).exists():
            Student.objects.create(**student_data)
            created += 1

    print(f"✓ {created} new sample student(s) created (total attempted: {len(students_data)})")

def create_sample_holidays():
    """Create sample holidays"""
    from attendance.models import Holiday, Teacher
    from datetime import date, timedelta

    teacher = Teacher.objects.first()
    if not teacher:
        print("✗ No teacher found, skipping holiday creation")
        return

    holidays_data = [
        {
            'date': date.today() + timedelta(days=10),
            'description': 'Independence Day',
        },
        {
            'date': date.today() + timedelta(days=25),
            'description': 'Labor Day',
        },
        {
            'date': date.today() + timedelta(days=45),
            'description': 'Thanksgiving Holiday',
        }
    ]

    created = 0
    for holiday_data in holidays_data:
        holiday_data['created_by'] = teacher
        if not Holiday.objects.filter(date=holiday_data['date']).exists():
            Holiday.objects.create(**holiday_data)
            created += 1

    print(f"✓ {created} new sample holiday(s) created (total attempted: {len(holidays_data)})")

def create_sample_attendance():
    """Create sample attendance records"""
    from attendance.models import Attendance, Student, Teacher
    from datetime import date, time, timedelta
    import random

    teacher = Teacher.objects.first()
    students = Student.objects.all()

    if not teacher or not students.exists():
        print("✗ No teacher or students found, skipping attendance creation")
        return

    created = 0
    # Create attendance for last 7 days
    for i in range(7):
        attendance_date = date.today() - timedelta(days=i)

        for student in students:
            # Random attendance (80% present)
            if random.random() < 0.8:  # 80% attendance rate
                if not Attendance.objects.filter(student=student, date=attendance_date).exists():
                    Attendance.objects.create(
                        student=student,
                        date=attendance_date,
                        time_in=time(9, random.randint(0, 30)),  # Between 9:00-9:30 AM
                        status='present',
                        marked_by=teacher
                    )
                    created += 1

    print(f"✓ {created} sample attendance record(s) created")

def main():
    """Main setup function"""
    print("🚀 Setting up Django Student Attendance Management System...")

    # Setup Django
    setup_django()

    # Run migrations
    print("\n📦 Running database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])

    # Create sample data
    print("\n👥 Creating sample data...")
    create_superuser()
    create_teacher()
    create_sample_students()
    create_sample_holidays()
    create_sample_attendance()

    print("\n✅ Setup completed successfully!")
    print("\n📋 Quick Start Guide:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Open http://127.0.0.1:8000 in your browser")
    print("3. Login with username: teacher, password: password123")
    print("4. Admin panel: http://127.0.0.1:8000/admin (username: admin, password: admin123)")
    print("\n🎯 Features available in this project:")
    print("- Manual/register-style attendance marking (teacher marks Present/Absent)")
    print("- Student management (CRUD operations)")
    print("- Holiday management")
    print("- Attendance reports and analytics")
    print("- Dashboard with attendance summary")

if __name__ == '__main__':
    main()
