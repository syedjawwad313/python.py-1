import sqlite3
import json
import csv
from typing import List, Optional, Dict, Any
from config import DATABASE_PATH, SUBJECTS
import database  # Ensure database tables are created

class StudentManager:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def add_student(self, student: Dict[str, Any]) -> None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (roll_no, name, age, gender, marks, total, percentage, grade)
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

    def update_student(self, roll_no: int, updated_fields: Dict[str, Any]) -> bool:
        conn = self._connect()
        cursor = conn.cursor()
        set_clause = []
        values = []
        for key, value in updated_fields.items():
            if key == 'marks':
                value = json.dumps(value)
            set_clause.append(f"{key} = ?")
            values.append(value)
        values.append(roll_no)
        query = f"UPDATE students SET {', '.join(set_clause)} WHERE roll_no = ?"
        cursor.execute(query, values)
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    def delete_student(self, roll_no: int) -> bool:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    def get_student(self, roll_no: int) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._row_to_dict(row)
        return None

    def get_all_students(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row: tuple) -> Dict[str, Any]:
        return {
            'roll_no': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'marks': json.loads(row[4]),
            'total': row[5],
            'percentage': row[6],
            'grade': row[7]
        }

    def find_highest_scorer(self) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY total DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._row_to_dict(row)
        return None

    def calculate_subject_averages(self) -> List[float]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT marks FROM students")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return [0.0] * len(SUBJECTS)
        totals = [0.0] * len(SUBJECTS)
        for (marks_json,) in rows:
            marks = json.loads(marks_json)
            for i, mark in enumerate(marks):
                totals[i] += mark
        count = len(rows)
        return [total / count for total in totals]

    def save_data(self) -> None:
        students = self.get_all_students()
        with open('data.json', 'w') as f:
            json.dump(students, f, indent=4)

    def import_students(self, students: List[Dict[str, Any]]) -> None:
        conn = self._connect()
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

    def export_csv(self, file_path: str) -> None:
        students = self.get_all_students()
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['roll_no', 'name', 'age', 'gender'] + SUBJECTS + ['total', 'percentage', 'grade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                row = {
                    'roll_no': student['roll_no'],
                    'name': student['name'],
                    'age': student['age'],
                    'gender': student['gender'],
                    'total': student['total'],
                    'percentage': student['percentage'],
                    'grade': student['grade']
                }
                for i, subject in enumerate(SUBJECTS):
                    row[subject] = student['marks'][i]
                writer.writerow(row)

    def import_csv(self, file_path: str) -> None:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            students = []
            for row in reader:
                marks = [float(row[subject]) for subject in SUBJECTS]
                student = {
                    'roll_no': int(row['roll_no']),
                    'name': row['name'],
                    'age': int(row['age']),
                    'gender': row['gender'],
                    'marks': marks,
                    'total': float(row['total']),
                    'percentage': float(row['percentage']),
                    'grade': row['grade']
                }
                students.append(student)
            self.import_students(students)
