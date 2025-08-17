import sqlite3

def check_admin_user():
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, user_type FROM Users WHERE username='admin';")
    user = cursor.fetchone()
    if user:
        print(f"user_id: {user[0]}, username: {user[1]}, user_type: {user[2]}")
    else:
        print("Admin user not found.")
    conn.close()

if __name__ == "__main__":
    check_admin_user()
