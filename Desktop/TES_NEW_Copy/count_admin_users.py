import sqlite3

def count_admin_users():
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE username='admin';")
    count = cursor.fetchone()[0]
    print(f"Number of users with username 'admin': {count}")
    conn.close()

if __name__ == "__main__":
    count_admin_users()
