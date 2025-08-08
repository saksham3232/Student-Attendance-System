# Django Student Attendance Management System

A comprehensive web-based attendance management system built with **Django**.

---

## Features

- 👥 **Student Management**: Complete CRUD operations for students  
- 📅 **Holiday Management**: Mark holidays and manage the academic calendar  
- 📊 **Analytics Dashboard**: Real-time attendance statistics and reports  
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices  
- 🔐 **Secure Authentication**: Teacher login system with role-based access  
- 🖊 **Manual Attendance**: Easy register-style attendance marking  

---

## Quick Installation

### 1. Extract and Setup

```bash
# Extract the ZIP file
# Navigate to project directory
cd student_attendance_system

# Create virtual environment
python -m venv attendance_env

# Activate virtual environment
# On Windows:
attendance_env\Scripts\activate

# On macOS/Linux:
source attendance_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Setup Script

```bash
python setup.py
```

### 4. Start Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

- Main Application: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin Panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

### Default Login Credentials

#### Teacher Login

- Username: `teacher`
- Password: `password123`

#### Admin Login

- Username: `admin`
- Password: `admin123`

---

## Project Structure

```
student_attendance_system/
├── manage.py
├── requirements.txt
├── setup.py
├── README.md
├── student_attendance/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── attendance/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   └── static/
└── media/
    └── student_photos/
```

---

## Usage Guide

### 1. Adding Students
- Navigate to "Students" in the sidebar
- Click "Add Student"
- Fill in student details
- Upload a student photo (optional)
- Save the student

### 2. Marking Attendance
- Go to "Mark Attendance"
- Select Present, Absent, or Late for each student
- Click Save Attendance
- Attendance is updated instantly

### 3. Managing Holidays
- Navigate to "Holidays"
- Add holiday dates and descriptions
- These dates are excluded from attendance calculations

### 4. Viewing Reports
- Go to "Reports"
- Select a date range
- View detailed attendance statistics

---

## Troubleshooting

### Common Issues

- Attendance not saving: Ensure all students have valid IDs in the database
- Date range issues in reports: Check that the end date is not earlier than the start date
- Static files not loading: Run `python manage.py collectstatic` in production

---

## Security Notes

⚠️ Configured for DEVELOPMENT only

For production deployment:

- Set `DEBUG = False` in `settings.py`
- Use a secure `SECRET_KEY`
- Switch from SQLite to PostgreSQL/MySQL
- Configure static/media file serving
- Set up HTTPS
- Add proper role-based permissions and error handling

---

## Support

For issues and questions:

- Check the troubleshooting section
- Review Django error logs in the terminal
- Ensure all dependencies are installed correctly

---

## License

This project is for educational purposes. You may modify and distribute it.
