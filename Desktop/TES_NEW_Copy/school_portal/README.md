# School Management Portal

A comprehensive school management system built with Flask and SQLite, designed to manage students, teachers, and administrative staff in an educational institution.

## Features

- **Role-based access control** (Students, Teachers, Management, Staff)
- **User authentication** (Login/Logout)
- **Dashboard** with overview and quick actions
- **Attendance tracking**
- **Class management**
- **Assignment management**
- **Responsive design** that works on all devices

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd school_portal
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python
   >>> from app import db, create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ```

## Running the Application

1. **Set the Flask app environment variable**
   - On Windows:
     ```cmd
     set FLASK_APP=app.py
     set FLASK_ENV=development
     ```
   - On macOS/Linux:
     ```bash
     export FLASK_APP=app.py
     export FLASK_ENV=development
     ```

2. **Run the application**
   ```bash
   flask run
   ```

3. **Access the application**
   Open your web browser and go to: http://127.0.0.1:5000/

## Creating Test Users

To create test users, you can use the Python shell:

```python
from app import create_app, db
from models import User, Student, Teacher, Management
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create a test student
    student_user = User(
        username='student1',
        email='student@example.com',
        first_name='John',
        last_name='Doe',
        user_type='student'
    )
    student_user.set_password('student123')
    db.session.add(student_user)
    db.session.commit()
    
    student = Student(
        user_id=student_user.user_id,
        admission_number='STD001',
        class_level='10A'
    )
    db.session.add(student)
    
    # Create a test teacher
    teacher_user = User(
        username='teacher1',
        email='teacher@example.com',
        first_name='Jane',
        last_name='Smith',
        user_type='teacher'
    )
    teacher_user.set_password('teacher123')
    db.session.add(teacher_user)
    db.session.commit()
    
    teacher = Teacher(
        user_id=teacher_user.user_id,
        employee_id='TCH001',
        specialization='Mathematics'
    )
    db.session.add(teacher)
    
    db.session.commit()
```

## Project Structure

```
school_portal/
├── app.py                 # Main application file
├── models.py              # Database models
├── requirements.txt       # Project dependencies
├── school_management.db   # SQLite database (created after first run)
├── static/                # Static files (CSS, JS, images)
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── dashboard.html     # Dashboard page
    ├── index.html         # Landing page
    └── login.html         # Login page
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or feedback, please contact the development team at support@schoolportal.edu
