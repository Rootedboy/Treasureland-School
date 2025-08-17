import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the current directory to the path so we can import app and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Teacher, Class

def extract_teacher_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    teachers = []
    
    # Find all teacher cards
    staff_cards = soup.find_all('div', class_='staff')
    
    for card in staff_cards:
        try:
            # Extract name
            name_elem = card.find('h3')
            if not name_elem:
                continue
                
            name = name_elem.text.strip()
            
            # Extract position/department
            position_elem = card.find('span', class_='position')
            position = position_elem.text.strip() if position_elem else "Teacher"
            
            # Determine if HOD (Head of Department)
            is_hod = 'HOD' in position.upper() or 'head' in position.lower() or 'director' in position.lower()
            
            # Extract department/class from section headers
            section = card.find_parent('section', class_='team-section')
            department = "Other"
            
            if section and 'id' in section.attrs:
                section_id = section['id']
                if 'admin' in section_id:
                    department = "Administration"
                elif 'teaching' in section_id:
                    department = "Teaching"
                elif 'ict' in section_id:
                    department = "ICT"
                elif 'music' in section_id:
                    department = "Music"
            
            # Find class/department from parent elements
            class_group = card.find_parent('div', class_='class-group')
            if class_group:
                h3 = class_group.find('h3')
                if h3:
                    department = h3.text.replace('Department', '').strip()
            
            # Generate email (firstname.lastname@school.com)
            email = f"{name.lower().replace(' ', '.')}@treasureland.sch.ng"
            
            # Default password (teachers will be asked to change on first login)
            password = "Teacher@123"
            
            teacher_data = {
                'name': name,
                'email': email,
                'password': password,
                'position': position,
                'department': department,
                'is_hod': is_hod,
                'date_of_birth': None,  # To be added later
                'qualifications': ""  # To be added later
            }
            
            teachers.append(teacher_data)
            
        except Exception as e:
            print(f"Error processing teacher card: {e}")
            continue
    
    return teachers

def import_teachers_to_db(teachers):
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        added = 0
        skipped = 0
        
        for teacher_data in teachers:
            # Check if teacher already exists
            if User.query.filter_by(email=teacher_data['email']).first():
                print(f"Skipping existing teacher: {teacher_data['name']}")
                skipped += 1
                continue
                
            try:
                # Create user
                name_parts = teacher_data['name'].split(' ')
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ""
                
                user = User(
                    username=teacher_data['email'].split('@')[0],
                    email=teacher_data['email'],
                    password_hash=generate_password_hash(teacher_data['password']),
                    first_name=first_name,
                    last_name=last_name,
                    phone_number='',
                    address='',
                    user_type='teacher',
                    date_created=datetime.utcnow()
                )
                
                db.session.add(user)
                db.session.flush()  # To get the user_id
                
                # Create teacher profile
                teacher = Teacher(
                    user_id=user.user_id,
                    employee_id=f"T{user.user_id:04d}",  # Generate employee ID
                    qualification="",  # To be added later
                    specialization=teacher_data['department'],
                    date_hired=datetime.utcnow()
                )
                
                db.session.add(teacher)
                db.session.commit()
                
                print(f"Added teacher: {teacher_data['name']} ({teacher_data['email']})")
                added += 1
                
            except Exception as e:
                db.session.rollback()
                print(f"Error adding teacher {teacher_data['name']}: {str(e)}")
                skipped += 1
        
        print(f"\nImport complete!")
        print(f"Added: {added}")
        print(f"Skipped (already exists): {skipped}")
        print(f"Total teachers in database: {User.query.filter_by(user_type='teacher').count()}")

if __name__ == '__main__':
    # Path to the HTML file
    html_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Treasureland_School', 'Our_Team.html')
    
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        print("Please make sure the path to 'Our_Team.html' is correct.")
        sys.exit(1)
    
    print("Extracting teacher data from HTML...")
    teachers = extract_teacher_data(html_file)
    
    if not teachers:
        print("No teachers found in the HTML file.")
        sys.exit(1)
    
    print(f"Found {len(teachers)} teachers in the HTML file.")
    print("\nSample teacher data:")
    for i, t in enumerate(teachers[:3], 1):
        print(f"{i}. {t['name']} - {t['position']} ({t['department']})")
    
    print("\nImporting teachers to database...")
    import_teachers_to_db(teachers)
