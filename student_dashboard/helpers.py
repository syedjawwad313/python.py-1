import json
import math
import logging
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Utility function to calculate percentage
def calculate_percentage(total_marks: float, max_marks: float) -> float:
    if max_marks == 0:
        raise ValueError("Max marks cannot be zero")
    return (total_marks / max_marks) * 100

# Function to assign grade based on percentage
def assign_grade(percentage: float) -> str:
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

# Recursive function to calculate factorial (for roll number)
def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Function to validate name (ensure no numbers)
def validate_name(name: str) -> str:
    if not all(c.isalpha() or c.isspace() for c in name):
        raise ValueError("Name must contain only letters and spaces")
    return name.strip()

# Function to calculate total marks
def calculate_total(marks: List[float]) -> float:
    return sum(marks)

# Function to find highest scorer
def find_highest_scorer(students: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not students:
        return None
    return max(students, key=lambda s: s['total'])

# Function to calculate average per subject
def calculate_subject_averages(students: List[Dict[str, Any]]) -> List[float]:
    if not students:
        return []
    num_subjects = len(students[0]['marks'])
    totals = [0.0] * num_subjects
    for student in students:
        for i, mark in enumerate(student['marks']):
            totals[i] += mark
    return [total / len(students) for total in totals]

# Function to save data to JSON (deprecated, use database)
def save_data(students: List[Dict[str, Any]], filename: str = 'data.json') -> None:
    with open(filename, 'w') as f:
        json.dump(students, f, indent=4)
    logging.info(f"Data saved to {filename}")

# Function to load data from JSON (deprecated, use database)
def load_data(filename: str = 'data.json') -> List[Dict[str, Any]]:
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
