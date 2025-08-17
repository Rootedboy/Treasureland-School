import os
import re
from app import app, db
from models import Teacher, User

def update_teacher_image_paths():
    """Update teacher image paths in the database based on existing image files."""
    # Get the path to the teacher_images directory
    image_dir = os.path.join(app.static_folder, 'teacher_images')
    
    if not os.path.exists(image_dir):
        print(f"Directory {image_dir} does not exist.")
        return
    
    # Get all image files in the directory
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if not image_files:
        print("No image files found in the directory.")
        return
    
    updated_count = 0
    
    # Process each image file
    for filename in image_files:
        # Extract teacher's name from filename (remove UUID prefix and file extension)
        teacher_name = re.sub(r'^[a-f0-9]{8}-(?:[a-f0-9]{4}-){3}[a-f0-9]{12}_', '', filename)
        teacher_name = os.path.splitext(teacher_name)[0]  # Remove file extension
        
        # Clean up the name - handle different patterns
        teacher_name = teacher_name.replace('_', ' ').replace('.', ' ').replace('-', ' ').strip()
        name_parts = [p for p in re.split(r'\s+', teacher_name) if p and len(p) > 1]
        
        # Try to find a matching teacher in the database
        # First, try to match by last name (assuming last name is more unique)
        last_name = teacher_name.split('_')[-1].strip()
        
        # Get all teachers
        all_teachers = Teacher.query.join(User).all()
        matched_teachers = []
        
        # Try different matching strategies
        for teacher in all_teachers:
            db_first = teacher.user.first_name.lower().replace('.', '').strip()
            db_last = teacher.user.last_name.lower().replace('.', '').strip()
            
            # Check if any part of the filename matches first or last name
            for part in name_parts:
                part = part.lower().replace('mrs', '').replace('mr', '').replace('miss', '').strip()
                if not part or len(part) < 2:
                    continue
                    
                # Check if this part matches first or last name
                if (part in db_first or part in db_last or 
                    db_first in part or db_last in part):
                    matched_teachers.append(teacher)
                    break
            
            # If we have a match, no need to check other teachers
            if matched_teachers:
                break
        
        if matched_teachers:
            # Update the first matching teacher
            teacher = matched_teachers[0]
            # Create the image path relative to the static folder
            image_path = os.path.join('teacher_images', filename).replace('\\', '/')
            teacher.image_path = image_path
            updated_count += 1
            print(f"Updated {teacher.user.first_name} {teacher.user.last_name} with image: {filename}")
        else:
            print(f"Could not find matching teacher for: {filename}")
    
    # Commit all changes to the database
    db.session.commit()
    print(f"\nUpdated image paths for {updated_count} teachers.")

if __name__ == '__main__':
    with app.app_context():
        update_teacher_image_paths()
