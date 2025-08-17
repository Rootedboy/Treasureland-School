from app import app, db
from models import User, Management, Student, Teacher, NonManagementStaff, Class, Attendance, StudentClassMapping
from werkzeug.security import generate_password_hash

def create_test_user():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Check if user already exists
        if not User.query.filter_by(email='admin@school.com').first():
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@school.com',
                first_name='Admin',
                last_name='User',
                user_type='management',
                phone_number='1234567890',
                address='School Address'
            )
            admin_user.set_password('admin123')
            
            # Add to database
            db.session.add(admin_user)
            db.session.commit()
            
            # Add to management
            management = Management(
                user_id=admin_user.user_id,
                position='System Administrator',
                department='Administration',
                responsibilities='System Management'
            )
            db.session.add(management)
            db.session.commit()
            
            print("Test admin user created successfully!")
            print("Email: admin@school.com")
            print("Password: admin123")
            print("You can now log in to the portal with these credentials.")
        else:
            print("Test user already exists!")

if __name__ == "__main__":
    create_test_user()
