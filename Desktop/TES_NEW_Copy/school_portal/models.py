from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    user_type = db.Column(db.String(20), nullable=False)  # student, teacher, management, staff
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='user', uselist=False, lazy=True)
    teacher = db.relationship('Teacher', backref='user', uselist=False, lazy=True)
    management = db.relationship('Management', backref='user', uselist=False, lazy=True)
    staff = db.relationship('NonManagementStaff', backref='user', uselist=False, lazy=True)
    
    @property
    def id(self):
        return self.user_id
        
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'Students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    class_level = db.Column(db.String(20))
    parent_name = db.Column(db.String(100))
    parent_contact = db.Column(db.String(50))
    
    # Relationships
    classes = db.relationship('Class', secondary='Student_Class_Mapping', back_populates='students')
    attendance_records = db.relationship('Attendance', back_populates='student')

class Teacher(db.Model):
    __tablename__ = 'Teachers'
    
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    qualification = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    date_hired = db.Column(db.Date)
    image_path = db.Column(db.String(255))  # Path to the teacher's profile image
    
    # Relationships
    classes = db.relationship('Class', backref='teacher', lazy=True)

class Management(db.Model):
    __tablename__ = 'Management'
    
    management_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    responsibilities = db.Column(db.Text)

class NonManagementStaff(db.Model):
    __tablename__ = 'Non_Management_Staff'
    
    staff_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('Management.management_id'))
    
    # Relationship
    supervisor = db.relationship('Management', backref='staff', lazy=True)

class Class(db.Model):
    __tablename__ = 'Classes'
    
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.teacher_id'))
    
    # Relationships
    students = db.relationship('Student', secondary='Student_Class_Mapping', back_populates='classes')

class StudentClassMapping(db.Model):
    __tablename__ = 'Student_Class_Mapping'
    
    mapping_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Students.student_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.class_id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'class_id', 'academic_year', name='unique_student_class_year'),
    )

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('Students.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late, excused
    notes = db.Column(db.Text)
    
    # Relationships
    student = db.relationship('Student', back_populates='attendance_records')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_attendance_per_day'),
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
