import unittest
from helpers import calculate_percentage, assign_grade, validate_name, calculate_total, calculate_subject_averages
from models import StudentManager
import os
import tempfile
import sqlite3

class TestHelpers(unittest.TestCase):
    def test_calculate_percentage(self):
        self.assertEqual(calculate_percentage(400, 500), 80.0)
        with self.assertRaises(ValueError):
            calculate_percentage(400, 0)

    def test_assign_grade(self):
        self.assertEqual(assign_grade(95), 'A+')
        self.assertEqual(assign_grade(85), 'A')
        self.assertEqual(assign_grade(75), 'B')
        self.assertEqual(assign_grade(65), 'C')
        self.assertEqual(assign_grade(55), 'D')
        self.assertEqual(assign_grade(45), 'F')

    def test_validate_name(self):
        self.assertEqual(validate_name("John Doe"), "John Doe")
        with self.assertRaises(ValueError):
            validate_name("John123")

    def test_calculate_total(self):
        self.assertEqual(calculate_total([80, 90, 85, 75, 70]), 400)

    def test_calculate_subject_averages(self):
        students = [
            {'marks': [80, 90, 85, 75, 70]},
            {'marks': [85, 95, 80, 80, 75]}
        ]
        averages = calculate_subject_averages(students)
        self.assertEqual(averages, [82.5, 92.5, 82.5, 77.5, 72.5])

class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.close(self.db_fd)  # Close the file descriptor
        self.manager = StudentManager(self.db_path)
        # Create the table in the temp db
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                marks TEXT,
                total REAL,
                percentage REAL,
                grade TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def tearDown(self):
        os.unlink(self.db_path)

    def test_add_and_get_student(self):
        student = {
            'roll_no': 1,
            'name': 'John Doe',
            'age': 20,
            'gender': 'M',
            'marks': [80, 90, 85, 75, 70],
            'total': 400,
            'percentage': 80.0,
            'grade': 'A'
        }
        self.manager.add_student(student)
        retrieved = self.manager.get_student(1)
        self.assertEqual(retrieved['name'], 'John Doe')

    def test_update_student(self):
        # Add student first
        student = {
            'roll_no': 1,
            'name': 'John Doe',
            'age': 20,
            'gender': 'M',
            'marks': [80, 90, 85, 75, 70],
            'total': 400,
            'percentage': 80.0,
            'grade': 'A'
        }
        self.manager.add_student(student)
        # Update
        updated = self.manager.update_student(1, {'name': 'Jane Doe'})
        self.assertTrue(updated)
        retrieved = self.manager.get_student(1)
        self.assertEqual(retrieved['name'], 'Jane Doe')

    def test_delete_student(self):
        # Add student first
        student = {
            'roll_no': 1,
            'name': 'John Doe',
            'age': 20,
            'gender': 'M',
            'marks': [80, 90, 85, 75, 70],
            'total': 400,
            'percentage': 80.0,
            'grade': 'A'
        }
        self.manager.add_student(student)
        # Delete
        deleted = self.manager.delete_student(1)
        self.assertTrue(deleted)
        retrieved = self.manager.get_student(1)
        self.assertIsNone(retrieved)

if __name__ == '__main__':
    unittest.main()
