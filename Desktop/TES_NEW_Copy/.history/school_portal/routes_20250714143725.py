from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from extensions import db
from models import User, Student, Teacher, Management, NonManagementStaff, Class, Attendance

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    import logging
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        logging.debug(f"Login attempt for username: {username}")
        user = User.query.filter_by(username=username).first()
        if user:
            logging.debug(f"Stored password hash for user {username}: {user.password_hash}")
            password_check = user.check_password(password)
            logging.debug(f"Password check result for user {username}: {password_check}")
            if password_check:
                login_user(user)
                next_page = request.args.get('next')
                logging.debug(f"User {username} logged in successfully.")
                return redirect(next_page or url_for('main.dashboard'))
            else:
                logging.debug(f"Password mismatch for user {username}.")
        else:
            logging.debug(f"User {username} not found.")
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    from datetime import datetime, timedelta
    
    # Prepare user data
    user_data = {
        'full_name': f"{current_user.first_name} {current_user.last_name}",
        'user_type': current_user.user_type.capitalize(),
        'email': current_user.email,
        'join_date': current_user.date_created.strftime('%B %Y')
    }
    
    # Prepare stats based on user type
    stats = {}
    upcoming_events = []
    
    if current_user.user_type == 'student':
        student = Student.query.filter_by(user_id=current_user.user_id).first()
        if student:
            stats = {
                'classes': len(student.classes),
                'attendance': 95,  # This should be calculated from attendance records
                'assignments': 5,  # This should be fetched from assignments
                'announcements': 3  # This should be fetched from announcements
            }
            
    elif current_user.user_type == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
        if teacher:
            stats = {
                'classes': Class.query.filter_by(teacher_id=teacher.teacher_id).count(),
                'students': 25,  # This should be calculated from student count in classes
                'assignments': 8,  # This should be fetched from assignments
                'announcements': 5  # This should be fetched from announcements
            }
    elif current_user.user_type == 'staff':
        # Placeholder for staff-specific stats
        stats = {
            'tasks': 10,  # Example placeholder
            'announcements': 2
        }
    elif current_user.user_type == 'management':
        # Placeholder for management-specific stats
        stats = {
            'reports': 4,  # Example placeholder
            'meetings': 3
        }
    
    # Sample upcoming events (replace with actual events from database)
    upcoming_events = [
        {'title': 'Math Class', 'date': '2025-07-14', 'time': '09:00 AM', 'type': 'class'},
        {'title': 'Science Quiz', 'date': '2025-07-15', 'time': '11:00 AM', 'type': 'exam'},
        {'title': 'Parent-Teacher Meeting', 'date': '2025-07-16', 'time': '02:00 PM', 'type': 'meeting'}
    ]
    
    return render_template('dashboard.html', 
                         user_data=user_data, 
                         stats=stats, 
                         upcoming_events=upcoming_events,
                         current_year=datetime.timezone.utc().year)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Add other routes here...
