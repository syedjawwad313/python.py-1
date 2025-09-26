import sqlite3
import json
from config import DATABASE_PATH, SUBJECTS

def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            marks TEXT,  -- JSON string for marks list
            total REAL,
            percentage REAL,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def migrate_from_json(json_file='data.json'):
    try:
        with open(json_file, 'r') as f:
            students = json.load(f)
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        for student in students:
            cursor.execute('''
                INSERT OR REPLACE INTO students (roll_no, name, age, gender, marks, total, percentage, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student['roll_no'],
                student['name'],
                student['age'],
                student['gender'],
                json.dumps(student['marks']),
                student['total'],
                student['percentage'],
                student['grade']
            ))
        conn.commit()
        conn.close()
        print("Migration from JSON to SQLite completed.")
    except FileNotFoundError:
        print("No JSON file found, starting fresh.")
    except Exception as e:
        print(f"Migration error: {e}")

# Initialize database
create_tables()
migrate_from_json()
