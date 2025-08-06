# Django Student Attendance Management System with Face Recognition

A comprehensive web-based attendance management system using Django and OpenCV face recognition technology.

## Features

- 🎭 **Face Recognition**: Real-time camera-based attendance marking
- 👥 **Student Management**: Complete CRUD operations for students
- 📅 **Holiday Management**: Mark holidays and manage academic calendar
- 📊 **Analytics Dashboard**: Real-time attendance statistics and reports
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- 🔐 **Secure Authentication**: Teacher login system with role-based access

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
- **Main Application**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## Default Login Credentials

### Teacher Login
- **Username**: teacher
- **Password**: password123

### Admin Login
- **Username**: admin  
- **Password**: admin123

## Project Structure

```
student_attendance_system/
├── manage.py
├── requirements.txt
├── setup.py
├── README.md
├── .env
├── student_attendance/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── attendance/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── face_recognition_utils.py
│   ├── templates/
│   └── static/
└── media/
    └── student_photos/
```

## Usage Guide

### 1. Adding Students
1. Navigate to "Students" in the sidebar
2. Click "Add Student"
3. Fill in student details
4. Upload a clear photo for face recognition
5. Save the student

### 2. Marking Attendance
1. Go to "Mark Attendance"
2. Click "Initialize Camera"
3. Click "Start Recognition"
4. Students' faces will be automatically recognized
5. Attendance is marked instantly

### 3. Managing Holidays
1. Navigate to "Holidays"
2. Add holiday dates and descriptions
3. These dates are excluded from attendance calculations

### 4. Viewing Reports
1. Go to "Reports"
2. Select date range
3. View detailed attendance statistics

## Troubleshooting

### Camera Issues
- **Camera not working**: Check browser permissions for camera access
- **Poor recognition**: Ensure good lighting and clear face visibility
- **HTTPS required**: Some browsers require HTTPS for camera access

### Installation Issues
- **dlib installation fails**: Install cmake first: `pip install cmake`
- **OpenCV issues**: Try: `pip install opencv-python-headless`
- **Face recognition fails**: Install: `pip install face-recognition --no-cache-dir`

## Security Notes

⚠️ **This is configured for DEVELOPMENT only**

For production deployment:
- Change `DEBUG = False` in settings.py
- Set secure `SECRET_KEY`
- Use PostgreSQL/MySQL instead of SQLite
- Configure proper static file serving
- Set up HTTPS
- Add proper error handling

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Ensure all dependencies are installed correctly
4. Verify camera permissions in browser

## License

This project is for educational purposes. Feel free to modify and distribute.
