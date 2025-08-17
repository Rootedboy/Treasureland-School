import sqlite3

def check_admin_password_hash():
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM Users WHERE username='admin';")
    result = cursor.fetchone()
    if result:
        print(f"Password hash for admin: {result[0]}")
    else:
        print("Admin user not found.")
    conn.close()

if __name__ == "__main__":
    check_admin_password_hash()
