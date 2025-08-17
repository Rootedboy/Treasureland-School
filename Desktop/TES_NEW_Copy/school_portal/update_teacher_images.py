import os
import shutil
from app import app, db
from models import Teacher, User
import re
from datetime import datetime

def sanitize_filename(name):
    """Convert a name to a safe filename"""
    # Remove special characters and replace spaces with underscores
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    return re.sub(r'[-\s]+', '-', name)

def update_teacher_images():
    base_dir = r'c:\Users\Tayo\Desktop\TES_New\Treasureland_School\images\CLASS GROUPS'
    image_dir = os.path.join(os.path.dirname(__file__), 'static', 'teacher_images')
    
    # Create the teacher_images directory if it doesn't exist
    os.makedirs(image_dir, exist_ok=True)
    
    # Dictionary to store teacher name -> image path mapping
    teacher_images = {}
    
    # Walk through all class directories to find teacher images
    for class_dir in os.listdir(base_dir):
        class_path = os.path.join(base_dir, class_dir)
        if not os.path.isdir(class_path):
            continue
            
        print(f"\nProcessing class: {class_dir}")
        
        # Process each image file in the directory
        for filename in os.listdir(class_path):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            # Skip group photos
            if any(x in filename.upper() for x in ['PRY', 'NURSERY', 'PLAY', 'CRECHE', 'PREPARATORY']):
                print(f"  Skipping group photo: {filename}")
                continue
            
            # Extract teacher name from filename (remove extension and split by _)
            teacher_name = os.path.splitext(filename)[0].split('_')[0].strip()
            if not teacher_name:
                print(f"  Could not extract name from: {filename}")
                continue
                
            src_path = os.path.join(class_path, filename)
            
            # Create a clean filename
            ext = os.path.splitext(filename)[1].lower()
            clean_name = sanitize_filename(teacher_name) + ext
            dest_path = os.path.join(image_dir, clean_name)
            
            # Copy the image file
            try:
                shutil.copy2(src_path, dest_path)
                teacher_images[teacher_name] = f"teacher_images/{clean_name}"
                print(f"  Copied image for {teacher_name}: {clean_name}")
            except Exception as e:
                print(f"  Error copying {filename}: {str(e)}")
    
    # Update the database with image paths
    with app.app_context():
        updated_count = 0
        
        for teacher_name, image_path in teacher_images.items():
            # Split name into parts
            name_parts = teacher_name.split()
            if len(name_parts) < 2:
                print(f"  Skipping incomplete name: {teacher_name}")
                continue
                
            last_name = name_parts[0]
            first_initial = name_parts[1][0] if name_parts[1] else ''
            
            # Find matching teachers
            teachers = Teacher.query.join(User).filter(
                db.and_(
                    db.or_(
                        User.last_name.ilike(f"{last_name}%"),
                        User.last_name.ilike(f"{last_name.split()[0]}%")
                    ),
                    User.first_name.ilike(f"{first_initial}%")
                )
            ).all()
            
            if not teachers:
                # Try just the last name
                teachers = Teacher.query.join(User).filter(
                    User.last_name.ilike(f"{last_name}%")
                ).all()
            
            if teachers:
                for teacher in teachers:
                    teacher.image_path = image_path
                    updated_count += 1
                    print(f"Updated image for {teacher.user.first_name} {teacher.user.last_name}: {image_path}")
            else:
                print(f"No match found for: {teacher_name}")
        
        # Commit all changes
        db.session.commit()
        print(f"\nUpdated {updated_count} teacher images in the database.")

if __name__ == '__main__':
    update_teacher_images()
