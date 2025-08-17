from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import Teacher, User, db

# Create a Blueprint for teacher routes
teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_bp.route('/')
@login_required
def list_teachers():
    if current_user.user_type not in ['management', 'admin']:
        flash('You do not have permission to view this page.', 'error')
        return redirect(url_for('main.dashboard'))
    
    teachers = Teacher.query.all()
    return render_template('teachers/list.html', teachers=teachers)

@teacher_bp.route('/<int:teacher_id>')
@login_required
def view_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('teachers/view.html', teacher=teacher)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'teacher_images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@teacher_bp.route('/edit/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    if current_user.user_type not in ['management', 'admin']:
        flash('You do not have permission to edit teacher profiles.', 'error')
        return redirect(url_for('main.dashboard'))
    
    teacher = Teacher.query.get_or_404(teacher_id)
    user = User.query.get(teacher.user_id)
    
    if request.method == 'POST':
        # Update user data
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        user.email = request.form.get('email', user.email)
        user.phone_number = request.form.get('phone_number', user.phone_number)
        user.address = request.form.get('address', user.address)
        
        # Update teacher data
        teacher.employee_id = request.form.get('employee_id', teacher.employee_id)
        teacher.hire_date = request.form.get('hire_date', teacher.hire_date)
        teacher.subject = request.form.get('subject', teacher.subject)
        teacher.qualification = request.form.get('qualification', teacher.qualification)
        teacher.emergency_contact = request.form.get('emergency_contact', teacher.emergency_contact)
        teacher.bio = request.form.get('bio', teacher.bio)
        
        # Handle file upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{teacher.teacher_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'teacher_images', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                teacher.profile_image = filename
        
        db.session.commit()
        flash('Teacher profile updated successfully!', 'success')
        return redirect(url_for('teacher.view_teacher', teacher_id=teacher.teacher_id))
    
    return render_template('teachers/edit.html', teacher=teacher, user=user)
