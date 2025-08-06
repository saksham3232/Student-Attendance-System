# attendance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
import json
import logging

from .models import Student, Teacher, Attendance, Holiday
from .forms import StudentForm, HolidayForm

logger = logging.getLogger(__name__)


def teacher_login(request):
    """Teacher login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'teacher'):
            login(request, user)
            messages.success(request, f'Welcome back, {user.teacher.name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not registered as a teacher')

    return render(request, 'attendance/login.html')


@login_required
def dashboard(request):
    """Main dashboard view"""
    total_students = Student.objects.filter(is_active=True).count()
    today = timezone.now().date()
    present_today = Attendance.objects.filter(date=today, status='present').count()

    if total_students > 0:
        attendance_percentage = (present_today / total_students) * 100
    else:
        attendance_percentage = 0

    recent_attendance = Attendance.objects.select_related('student').filter(
        date=today
    ).order_by('-created_timestamp')[:10]

    upcoming_holidays = Holiday.objects.filter(
        date__gte=today
    ).order_by('date')[:5]

    weekly_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        present_count = Attendance.objects.filter(date=date, status='present').count()
        weekly_data.append({
            'date': date.strftime('%m/%d'),
            'present': present_count
        })
    weekly_data.reverse()

    context = {
        'total_students': total_students,
        'present_today': present_today,
        'attendance_percentage': round(attendance_percentage, 1),
        'recent_attendance': recent_attendance,
        'upcoming_holidays': upcoming_holidays,
        'current_date': today,
        'weekly_data': json.dumps(weekly_data),
    }

    return render(request, 'attendance/dashboard.html', context)


@login_required
def student_list(request):
    """List all students"""
    students = Student.objects.filter(is_active=True).order_by('name')

    for student in students:
        total_days = Attendance.objects.filter(student=student).count()
        present_days = Attendance.objects.filter(student=student, status='present').count()

        if total_days > 0:
            student.attendance_percentage = round((present_days / total_days) * 100, 1)
        else:
            student.attendance_percentage = 0

        student.total_days = total_days
        student.present_days = present_days

    return render(request, 'attendance/student_list.html', {'students': students})


@login_required
def student_create(request):
    """Create new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'attendance/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_update(request, pk):
    """Update student"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            updated_student = form.save(commit=False)
            updated_student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'attendance/student_form.html', {
        'form': form,
        'title': 'Update Student',
        'student': student
    })


@login_required
def student_delete(request, pk):
    """Soft-delete (deactivate) student"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'Student {student.name} deactivated successfully!')
        return redirect('student_list')

    return render(request, 'attendance/student_confirm_delete.html', {'student': student})


@login_required
def mark_attendance(request):
    """
    Register-style attendance marking for the current date.
    Shows a list of active students with Present/Absent/Late options.
    Submits a bulk POST to create/update Attendance for today's date.
    """
    # Use the global timezone imported at module level (don't import inside the function)
    today = timezone.now().date()

    # Ensure the request user has a teacher profile
    if not hasattr(request.user, 'teacher'):
        messages.error(request, 'You are not authorized to mark attendance.')
        return redirect('teacher_login')

    teacher = request.user.teacher

    if request.method == 'POST':
        # Expect POST data in form: attendance-<student_id> = 'present'/'absent'/'late'
        submitted = {k: v for k, v in request.POST.items() if k.startswith('attendance-')}

        if not submitted:
            messages.error(request, 'No attendance data submitted.')
            return redirect('mark_attendance')

        success_count = 0
        for key, status in submitted.items():
            # key format: attendance-<student_id>
            try:
                _, student_id = key.split('-', 1)
                # If Student.student_id is numeric string in your model, ensure matching type; here
                # we assume the field is unique and can be matched by whatever type stored.
                student = Student.objects.get(student_id=student_id, is_active=True)
            except (ValueError, Student.DoesNotExist):
                logger.warning(f"Invalid attendance key or student not found: {key}")
                continue

            # Create or update attendance for today
            attendance_values = {
                'status': status,
                'marked_by': teacher,
            }

            local_time = timezone.localtime(timezone.now()).time()

            if status == 'present':
                attendance_values['time_in'] = local_time
            else:
                attendance_values['time_in'] = None

            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults=attendance_values
            )
            success_count += 1

        messages.success(request, f'Attendance updated for {success_count} students for {today}')
        return redirect('dashboard')

    else:
        students = Student.objects.filter(is_active=True).order_by('name')

        # Prefill existing attendance for today so radios can be pre-selected in template
        existing_attendance = Attendance.objects.filter(date=today)
        # Map by student_id (ensure keys match the same type you use in templates)
        existing_map = {a.student.student_id: a for a in existing_attendance}

        student_rows = []
        for s in students:
            a = existing_map.get(s.student_id)
            student_rows.append({
                'student': s,
                'status': a.status if a else 'absent'  # default to absent
            })

        return render(request, 'attendance/mark_attendance.html', {
            'students': student_rows,
            'current_date': today
        })


@login_required
def holiday_management(request):
    """Manage holidays"""
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save(commit=False)
            # safe check: ensure request.user has teacher attribute
            if hasattr(request.user, 'teacher'):
                holiday.created_by = request.user.teacher
            holiday.save()
            messages.success(request, f'Holiday \"{holiday.description}\" added successfully!')
            return redirect('holiday_management')
    else:
        form = HolidayForm()

    holidays = Holiday.objects.all().order_by('-date')
    return render(request, 'attendance/holiday_management.html', {
        'form': form,
        'holidays': holidays
    })


@login_required
def delete_holiday(request, pk):
    """Delete holiday"""
    if request.method == 'POST':
        holiday = get_object_or_404(Holiday, pk=pk)
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully!')

    return redirect('holiday_management')


from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance, Holiday  # adjust as per your models

def parse_date_safe(date_str, fallback):
    """Parses a date string (YYYY-MM-DD) into a date object. Falls back if empty or invalid."""
    if not date_str:
        return fallback
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return fallback

@login_required
def attendance_report(request):
    """Generate attendance reports (defaults to current date when no filters provided)."""
    students = Student.objects.filter(is_active=True)
    today = timezone.now().date()

    # Parse GET parameters safely
    raw_start = request.GET.get("start_date", "")
    raw_end = request.GET.get("end_date", "")
    
    start_date = parse_date_safe(raw_start, today)
    end_date = parse_date_safe(raw_end, today)

    # If end date is before start, fix it
    if end_date < start_date:
        end_date = start_date

    # Fetch holidays in range
    holidays = Holiday.objects.filter(date__range=[start_date, end_date])
    holiday_dates = set(h.date for h in holidays)

    # Count working days (Mon–Fri excluding holidays)
    total_working_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in holiday_dates:
            total_working_days += 1
        current_date += timedelta(days=1)

    # Build report
    report_data = []
    for student in students:
        present_days = Attendance.objects.filter(
            student=student,
            date__range=[start_date, end_date],
            status='present'
        ).count()

        absent_days = total_working_days - present_days

        attendance_percentage = (
            (present_days / total_working_days) * 100
            if total_working_days > 0 else 0.0
        )

        report_data.append({
            'student': student,
            'present_days': present_days,
            'absent_days': absent_days,
            'total_working_days': total_working_days,
            'attendance_percentage': round(attendance_percentage, 1)
        })

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'total_working_days': total_working_days,
        'holidays': holidays,
    }

    return render(request, 'attendance/attendance_report.html', context)


@login_required
def teacher_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('teacher_login')


@login_required
def get_student_attendance_data(request, student_id):
    """Get attendance data for a specific student"""
    try:
        student = Student.objects.get(student_id=student_id)

        today = timezone.now().date()
        start_date = today - timedelta(days=30)

        attendance_records = Attendance.objects.filter(
            student=student,
            date__range=[start_date, today]
        ).order_by('date')

        data = []
        for record in attendance_records:
            data.append({
                'date': record.date.strftime('%Y-%m-%d'),
                'status': record.status,
                'time_in': record.time_in.strftime('%H:%M') if record.time_in else None,
            })

        return JsonResponse({
            'success': True,
            'student_name': student.name,
            'data': data
        })

    except Student.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Student not found'
        })


# @login_required
# def manual_attendance(request):
#     """
#     Kept for single-student manual entries if needed.
#     This view previously existed; it accepts a student_id, date, and status and creates/updates that record.
#     """
#     local_time = timezone.localtime(timezone.now()).time()

#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         date_str = request.POST.get('date')
#         status = request.POST.get('status')

#         # Parse date; if invalid, use today
#         try:
#             attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
#         except (ValueError, TypeError):
#             attendance_date = timezone.now().date()

#         try:
#             student = Student.objects.get(student_id=student_id)
#             teacher = getattr(request.user, 'teacher', None)

#             attendance, created = Attendance.objects.get_or_create(
#                 student=student,
#                 date=attendance_date,
#                 defaults={
#                     'status': status,
#                     'marked_by': teacher,
#                     'time_in': local_time if status == 'present' else None,
#                 }
#             )

#             if not created:
#                 attendance.status = status
#                 attendance.marked_by = teacher
#                 if status == 'present':
#                     attendance.time_in = timezone.now().time()
#                 else:
#                     attendance.time_in = None
#                 attendance.save()

#             messages.success(request, f'Manual attendance marked for {student.name}')

#         except Student.DoesNotExist:
#             messages.error(request, 'Student not found')

#     students = Student.objects.filter(is_active=True).order_by('name')
#     today = timezone.now().date()
#     return render(request, 'attendance/manual_attendance.html', {'students': students, 'today': today})
