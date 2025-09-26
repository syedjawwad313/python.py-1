from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    calculate_percentage, assign_grade, calculate_total, validate_name,
    find_highest_scorer, calculate_subject_averages
)
from models import StudentManager
from config import SUBJECTS, MAX_MARKS_PER_SUBJECT, TOTAL_MAX_MARKS

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Initialize student manager
manager = StudentManager()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            name = validate_name(request.form['name'])
            roll_no = int(request.form['roll_no'])
            age = int(request.form['age'])
            gender = request.form['gender'].upper()
            if gender not in ['M', 'F']:
                raise ValueError("Gender must be M or F")
            marks = []
            for subject in SUBJECTS:
                mark = float(request.form[subject.lower()])
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
            flash(f"Student {name} added successfully!", "success")
            return redirect(url_for('home'))
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Unexpected error: {e}", "error")
    return render_template('add_student.html', subjects=SUBJECTS)

@app.route('/display')
def display_students():
    students = manager.get_all_students()
    return render_template('display_students.html', students=students)

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    student = None
    if request.method == 'POST':
        try:
            roll_no = int(request.form['roll_no'])
            student = manager.get_student(roll_no)
            if not student:
                flash("Student not found.", "error")
        except ValueError:
            flash("Invalid roll number.", "error")
    return render_template('search_student.html', student=student, subjects=SUBJECTS)

@app.route('/statistics')
def show_statistics():
    highest = manager.find_highest_scorer()
    averages = manager.calculate_subject_averages()
    return render_template('statistics.html', highest=highest, averages=averages, subjects=SUBJECTS)

@app.route('/edit/<int:roll_no>', methods=['GET', 'POST'])
def edit_student(roll_no):
    student = manager.get_student(roll_no)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for('home'))
    if request.method == 'POST':
        try:
            name = validate_name(request.form['name'])
            age = int(request.form['age'])
            gender = request.form['gender'].upper()
            if gender not in ['M', 'F']:
                raise ValueError("Gender must be M or F")
            marks = []
            for subject in SUBJECTS:
                mark = float(request.form[subject.lower()])
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
                flash(f"Student {name} updated successfully!", "success")
                return redirect(url_for('home'))
            else:
                flash("Failed to update student.", "error")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Unexpected error: {e}", "error")
    return render_template('edit_student.html', student=student, subjects=SUBJECTS)

@app.route('/delete/<int:roll_no>', methods=['POST'])
def delete_student(roll_no):
    if manager.delete_student(roll_no):
        flash("Student deleted successfully!", "success")
    else:
        flash("Student not found.", "error")
    return redirect(url_for('display_students'))

if __name__ == '__main__':
    app.run(debug=True)
