import os

# Configuration settings
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'students.db')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'app.log')
SUBJECTS = ['Math', 'Science', 'English', 'History', 'Art']
MAX_MARKS_PER_SUBJECT = 100
TOTAL_MAX_MARKS = len(SUBJECTS) * MAX_MARKS_PER_SUBJECT
