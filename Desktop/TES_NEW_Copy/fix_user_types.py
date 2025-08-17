import sqlite3

def fix_user_types():
    valid_types = ('student', 'teacher', 'management', 'staff')
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, user_type FROM Users")
    users = cursor.fetchall()
    for user_id, user_type in users:
        if user_type not in valid_types:
            cursor.execute("UPDATE Users SET user_type='staff' WHERE user_id=?", (user_id,))
            print(f"Updated user_type for user_id {user_id} from {user_type} to 'staff'")
    conn.commit()
    conn.close()
    print("User type fix complete.")

if __name__ == "__main__":
    fix_user_types()
