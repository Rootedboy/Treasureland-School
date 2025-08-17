from app import app, db
from models import User, Student, Teacher, Management, NonManagementStaff, Class, Attendance
from werkzeug.security import generate_password_hash

def create_tables():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create sample data if no users exist
        if not User.query.first():
            # Create sample users
            users = [
                User(
                    username='admin',
                    email='admin@school.com',
                    password_hash=generate_password_hash('admin123'),
                    user_type='admin',
                    first_name='Admin',
                    last_name='User'
                ),
                User(
                    username='johndoe',
                    email='teacher@school.com',
                    password_hash=generate_password_hash('teacher123'),
                    user_type='teacher',
                    first_name='John',
                    last_name='Doe'
                ),
                User(
                    username='alice.smith',
                    email='student@school.com',
                    password_hash=generate_password_hash('student123'),
                    user_type='student',
                    first_name='Alice',
                    last_name='Smith'
                )
            ]
            
            db.session.add_all(users)
            db.session.commit()
            
            print("Sample data created successfully")
        
        print("Database tables created and initialized successfully")

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
