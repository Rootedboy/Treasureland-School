import sqlite3
from datetime import datetime

def create_database():
    # Connect to SQLite database (will be created if it doesn't exist)
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Create Users table (base table for all user types)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE,
        phone_number TEXT,
        address TEXT,
        user_type TEXT NOT NULL CHECK(user_type IN ('student', 'teacher', 'management', 'staff')),
        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        admission_number TEXT UNIQUE NOT NULL,
        class_level TEXT,
        parent_name TEXT,
        parent_contact TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Teachers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        employee_id TEXT UNIQUE NOT NULL,
        qualification TEXT,
        specialization TEXT,
        date_hired DATE,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Management table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Management (
        management_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        position TEXT NOT NULL,
        department TEXT,
        responsibilities TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Non_Management_Staff table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Non_Management_Staff (
        staff_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        position TEXT NOT NULL,
        department TEXT,
        supervisor_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (supervisor_id) REFERENCES Management(management_id)
    )
    ''')

    # Create Classes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classes (
        class_id INTEGER PRIMARY KEY,
        class_name TEXT NOT NULL,
        academic_year TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
    )
    ''')

    # Create Student_Class_Mapping table (for many-to-many relationship between students and classes)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student_Class_Mapping (
        mapping_id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        class_id INTEGER NOT NULL,
        academic_year TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (class_id) REFERENCES Classes(class_id),
        UNIQUE(student_id, class_id, academic_year)
    )
    ''')

    # Create Attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attendance (
        attendance_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'excused')),
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON Users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_admission ON Students(admission_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_date ON Attendance(date)')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database 'school_management.db' has been created successfully!")

if __name__ == "__main__":
    create_database()
