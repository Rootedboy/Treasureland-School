import os
import re
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from app import create_app
from models import db
from sqlalchemy.orm import joinedload
import sys

def extract_teacher_info(filename):
    """Extract teacher name and class from filename"""
    # Remove file extension and split by underscores
    base_name = os.path.splitext(filename)[0]
    
    # Pattern to match teacher name and class
    # Example: "MGBOLU M. I_Primary 1_Hod_Yellow.jpg"
    # or "FAJEMIDAGBA M. B_Yellow.jpg"
    
    # Try to match the longer pattern first (with HOD)
    match = re.match(r'^([^_]+)_(.+?)(?:_Hod)?_(\w+)$', base_name)
    if match:
        name = match.group(1).strip()
        class_info = f"{match.group(2).strip()} {match.group(3).strip()}"
        return name, class_info
    
    # Try simpler pattern if the first one doesn't match
    match = re.match(r'^([^_]+)_(\w+)$', base_name)
    if match:
        name = match.group(1).strip()
        class_info = match.group(2).strip()
        return name, class_info
    
    return None, None

def update_teacher_classes():
    base_dir = r'c:\Users\Tayo\Desktop\TES_New\Treasureland_School\images\CLASS GROUPS'
    
    # Dictionary to store teacher -> [classes] mapping
    teacher_classes = {}
    
    # Walk through all class directories
    for class_dir in os.listdir(base_dir):
        class_path = os.path.join(base_dir, class_dir)
        if not os.path.isdir(class_path):
            continue
            
        print(f"\nProcessing class: {class_dir}")
        
        # Process each file in the directory
        for filename in os.listdir(class_path):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            teacher_name, class_info = extract_teacher_info(filename)
            if not teacher_name:
                print(f"  Could not parse: {filename}")
                continue
                
            # Clean up the class info
            class_info = class_info.replace('_', ' ').strip()
            
            # Initialize teacher in dictionary if not exists
            if teacher_name not in teacher_classes:
                teacher_classes[teacher_name] = set()
            
            # Add this class to the teacher's classes
            teacher_classes[teacher_name].add(f"{class_dir} {class_info}")
            
            print(f"  {teacher_name} -> {class_dir} {class_info}")
    
    # Now update the database
    with app.app_context():
        updated_count = 0
        
        for teacher_name, classes in teacher_classes.items():
            # Try to find the teacher by name
            # The name in the filename might be in "LAST F. M" format
            # So we'll split and search for first and last names
            name_parts = teacher_name.split()
            
            if len(name_parts) >= 2:
                # Try to match last name and first initial
                last_name = name_parts[0]
                first_initial = name_parts[1][0]
                
                # Query for teachers with matching last name and first initial
                teachers = Teacher.query.join(User).filter(
                    User.last_name.ilike(f"{last_name}%"),
                    User.first_name.ilike(f"{first_initial}%")
                ).all()
                
                if teachers:
                    if len(teachers) > 1:
                        print(f"\nMultiple matches for {teacher_name}:")
                        for i, t in enumerate(teachers, 1):
                            print(f"  {i}. {t.user.first_name} {t.user.last_name} ({t.employee_id})")
                        
                        # For now, just take the first match
                        teacher = teachers[0]
                        print(f"  Using first match: {teacher.user.first_name} {teacher.user.last_name}")
                    else:
                        teacher = teachers[0]
                    
                    # Update the teacher's specialization with their classes
                    class_list = ", ".join(sorted(classes))
                    teacher.specialization = class_list
                    updated_count += 1
                    print(f"Updated {teacher.user.first_name} {teacher.user.last_name}: {class_list}")
                else:
                    print(f"No match found for: {teacher_name}")
        
        # Commit all changes
        db.session.commit()
        print(f"\nUpdated {updated_count} teachers with class assignments.")

if __name__ == '__main__':
    # Add the parent directory to the path so we can import app and models
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)
    
    update_teacher_classes()
