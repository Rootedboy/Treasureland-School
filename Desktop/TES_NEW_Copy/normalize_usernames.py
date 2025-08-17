import sqlite3

def normalize_usernames():
    conn = sqlite3.connect('school_portal/school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM Users")
    users = cursor.fetchall()
    for user_id, username in users:
        normalized_username = username.strip().lower()
        if username != normalized_username:
            cursor.execute("UPDATE Users SET username=? WHERE user_id=?", (normalized_username, user_id))
            print(f"Normalized username for user_id {user_id}: {username} -> {normalized_username}")
    conn.commit()
    conn.close()
    print("Username normalization complete.")

if __name__ == "__main__":
    normalize_usernames()
