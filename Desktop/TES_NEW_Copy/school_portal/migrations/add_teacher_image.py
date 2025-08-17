import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, db
from sqlalchemy import text

def upgrade():
    with app.app_context():
        # Check if column exists first
        with db.engine.connect() as connection:
            # SQLite doesn't support IF NOT EXISTS in ADD COLUMN, so we need to check first
            result = connection.execute(text("""
                SELECT COUNT(*) AS count FROM pragma_table_info('Teachers') WHERE name='image_path';
            """)).scalar()
            
            if result == 0:
                connection.execute(text("""
                    ALTER TABLE Teachers 
                    ADD COLUMN image_path VARCHAR(255);
                """))
                connection.commit()
                print("Added image_path column to Teachers table")
            else:
                print("image_path column already exists in Teachers table")

def downgrade():
    with app.app_context():
        # Check if column exists first
        with db.engine.connect() as connection:
            result = connection.execute(text("""
                SELECT COUNT(*) AS count FROM pragma_table_info('Teachers') WHERE name='image_path';
            """)).scalar()
            
            if result > 0:
                # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
                connection.execute(text("""
                    CREATE TABLE Teachers_new (
                        teacher_id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        employee_id VARCHAR(50),
                        qualification TEXT,
                        specialization TEXT,
                        date_hired DATE,
                        FOREIGN KEY (user_id) REFERENCES Users(user_id)
                    );
                    
                    INSERT INTO Teachers_new (teacher_id, user_id, employee_id, qualification, specialization, date_hired)
                    SELECT teacher_id, user_id, employee_id, qualification, specialization, date_hired
                    FROM Teachers;
                    
                    DROP TABLE Teachers;
                    ALTER TABLE Teachers_new RENAME TO Teachers;
                """))
                connection.commit()
                print("Removed image_path column from Teachers table")
            else:
                print("image_path column does not exist in Teachers table")

if __name__ == '__main__':
    with app.app_context():
        upgrade()
