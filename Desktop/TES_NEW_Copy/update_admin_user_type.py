import sqlite3

def update_admin_user_type():
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET user_type='staff' WHERE username='admin';")
    conn.commit()
    print("Admin user_type updated to 'staff'.")
    conn.close()

if __name__ == "__main__":
    update_admin_user_type()
