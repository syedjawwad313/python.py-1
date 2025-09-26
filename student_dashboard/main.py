import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    calculate_percentage, assign_grade, calculate_total, validate_name,
    find_highest_scorer, calculate_subject_averages, factorial
)
from models import StudentManager
from config import SUBJECTS, MAX_MARKS_PER_SUBJECT, TOTAL_MAX_MARKS

# Initialize student manager
manager = StudentManager()

def get_student_input():
    try:
        name = input("Enter student's name: ")
        name = validate_name(name)
        roll_no = int(input("Enter roll number: "))
        age = int(input("Enter age: "))
        gender = input("Enter gender (M/F): ").upper()
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be M or F")
        marks = []
        for subject in SUBJECTS:
            mark = float(input(f"Enter marks for {subject}: "))
            if mark < 0 or mark > MAX_MARKS_PER_SUBJECT:
                raise ValueError(f"Marks for {subject} must be between 0 and {MAX_MARKS_PER_SUBJECT}")
            marks.append(mark)
        total = calculate_total(marks)
        percentage = calculate_percentage(total, TOTAL_MAX_MARKS)
        grade = assign_grade(percentage)
        student = {
            'name': name,
            'roll_no': roll_no,
            'age': age,
            'gender': gender,
            'marks': marks,
            'total': total,
            'percentage': percentage,
            'grade': grade
        }
        manager.add_student(student)
        print(f"Student {name} added successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def display_students():
    students = manager.get_all_students()
    if not students:
        print("No students to display.")
        return
    for student in students:
        print(f"Name: {student['name']}, Roll No: {student['roll_no']}, Total: {student['total']}, Percentage: {student['percentage']:.2f}%, Grade: {student['grade']}")

def search_student():
    try:
        roll_no = int(input("Enter roll number to search: "))
        student = manager.get_student(roll_no)
        if student:
            print(f"Name: {student['name']}, Age: {student['age']}, Gender: {student['gender']}")
            print(f"Marks: {dict(zip(SUBJECTS, student['marks']))}")
            print(f"Total: {student['total']}, Percentage: {student['percentage']:.2f}%, Grade: {student['grade']}")
        else:
            print("Student not found.")
    except ValueError:
        print("Invalid roll number.")

def show_statistics():
    highest = manager.find_highest_scorer()
    if highest:
        print(f"Highest Scorer: {highest['name']} with {highest['total']} marks")
    else:
        print("No data available.")
        return
    averages = manager.calculate_subject_averages()
    print("Subject Averages:")
    for subject, avg in zip(SUBJECTS, averages):
        print(f"{subject}: {avg:.2f}")

def edit_student():
    try:
        roll_no = int(input("Enter roll number to edit: "))
        student = manager.get_student(roll_no)
        if not student:
            print("Student not found.")
            return
        print("Current details:")
        print(f"Name: {student['name']}, Age: {student['age']}, Gender: {student['gender']}")
        print(f"Marks: {dict(zip(SUBJECTS, student['marks']))}")
        # For simplicity, allow editing name and age
        name = input(f"Enter new name (current: {student['name']}): ") or student['name']
        name = validate_name(name)
        age = int(input(f"Enter new age (current: {student['age']}): ") or student['age'])
        gender = input(f"Enter new gender M/F (current: {student['gender']}): ").upper() or student['gender']
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be M or F")
        marks = []
        for i, subject in enumerate(SUBJECTS):
            mark_input = input(f"Enter new marks for {subject} (current: {student['marks'][i]}): ")
            if mark_input.strip() == "":
                mark = student['marks'][i]
            else:
                mark = float(mark_input)
            if mark < 0 or mark > MAX_MARKS_PER_SUBJECT:
                raise ValueError(f"Marks for {subject} must be between 0 and {MAX_MARKS_PER_SUBJECT}")
            marks.append(mark)
        total = calculate_total(marks)
        percentage = calculate_percentage(total, TOTAL_MAX_MARKS)
        grade = assign_grade(percentage)
        updated_fields = {
            'name': name,
            'age': age,
            'gender': gender,
            'marks': marks,
            'total': total,
            'percentage': percentage,
            'grade': grade
        }
        if manager.update_student(roll_no, updated_fields):
            print("Student updated successfully!")
        else:
            print("Failed to update student.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def delete_student():
    try:
        roll_no = int(input("Enter roll number to delete: "))
        if manager.delete_student(roll_no):
            print("Student deleted successfully!")
        else:
            print("Student not found.")
    except ValueError:
        print("Invalid roll number.")

def main_menu():
    while True:
        print("\nStudent Performance Management System")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Edit Student")
        print("5. Delete Student")
        print("6. Show Statistics")
        print("7. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            get_student_input()
        elif choice == '2':
            display_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            edit_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            show_statistics()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    print("Welcome to the Student Performance Management System!")
    main_menu()
