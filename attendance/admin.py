from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Teacher, Student, Holiday, Attendance


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']
    search_fields = ['name', 'subject']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'email', 'is_active', 'created_date']
    list_filter = ['is_active', 'created_date']
    search_fields = ['student_id', 'name', 'email']
    ordering = ['student_id']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'description', 'created_by', 'created_date']
    list_filter = ['date', 'created_by']
    search_fields = ['description', 'created_by__name']
    date_hierarchy = 'date'


def mark_present(modeladmin, request, queryset):
    """Admin action — mark selected attendance records as present (sets time_in to now)."""
    from django.utils import timezone
    now = timezone.now().time()
    updated = queryset.update(status='present', time_in=now)
    modeladmin.message_user(request, f"{updated} record(s) marked as Present.")


mark_present.short_description = "Mark selected attendance as Present"


def mark_absent(modeladmin, request, queryset):
    """Admin action — mark selected attendance records as absent (clears time_in)."""
    updated = queryset.update(status='absent', time_in=None)
    modeladmin.message_user(request, f"{updated} record(s) marked as Absent.")


mark_absent.short_description = "Mark selected attendance as Absent"


def export_attendance_csv(modeladmin, request, queryset):
    """Export selected attendance records as CSV."""
    meta = modeladmin.model._meta
    field_names = ['student__student_id', 'student__name', 'date', 'status', 'time_in', 'time_out', 'marked_by__name', 'created_timestamp']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=attendance_export.csv'
    writer = csv.writer(response)

    # Header
    writer.writerow(['Student ID', 'Student Name', 'Date', 'Status', 'Time In', 'Time Out', 'Marked By', 'Created Timestamp'])

    for obj in queryset.select_related('student', 'marked_by'):
        writer.writerow([
            obj.student.student_id,
            obj.student.name,
            obj.date.isoformat(),
            obj.status,
            obj.time_in.isoformat() if obj.time_in else '',
            obj.time_out.isoformat() if obj.time_out else '',
            obj.marked_by.name if obj.marked_by else '',
            obj.created_timestamp.isoformat() if obj.created_timestamp else '',
        ])

    return response


export_attendance_csv.short_description = "Export selected attendance to CSV"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'time_in', 'time_out', 'marked_by', 'created_timestamp']
    list_filter = ['status', 'date', 'marked_by']
    search_fields = ['student__name', 'student__student_id']
    date_hierarchy = 'date'
    readonly_fields = ['created_timestamp']
    actions = [mark_present, mark_absent, export_attendance_csv]
    list_select_related = ('student', 'marked_by')
    ordering = ['-date', 'student__student_id']
