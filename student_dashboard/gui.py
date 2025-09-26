"""
Student Performance Management System - GUI Application
Tkinter-based graphical user interface for student management using SQLite
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    calculate_percentage, assign_grade, calculate_total, validate_name
)
from models import StudentManager
from config import SUBJECTS, MAX_MARKS_PER_SUBJECT, TOTAL_MAX_MARKS

class StudentDashboardApp:
    def __init__(self):
        self.manager = StudentManager()
        self.students = self.manager.get_all_students()
        self.root = tk.Tk()
        self.root.title("Student Performance Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Set ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Professional theme
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'), padding=[10, 5])
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=[5, 5])
        self.style.configure('TEntry', font=('Arial', 10))

        self.create_menu()
        self.create_toolbar()
        self.create_tabs()
        self.create_status_bar()

        # Use grid layout for professional structure
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.toolbar.grid(row=0, column=0, sticky='ew')
        self.tab_control.grid(row=1, column=0, sticky='nsew')
        self.status_bar.grid(row=2, column=0, sticky='ew')

        # Initial load
        self.display_students()
        self.show_statistics()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Export to JSON", command=self.export_json)
        file_menu.add_command(label="Import from JSON", command=self.import_json)
        file_menu.add_command(label="Export to CSV", command=self.export_csv)
        file_menu.add_command(label="Import from CSV", command=self.import_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh Display", command=self.display_students)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.help_menu)

    def help_menu(self):
        messagebox.showinfo("Help", "Student Performance Management System\n\nFeatures:\n- Add Students\n- View Students\n- Search Students\n- Edit/Delete Students\n- View Statistics\n\nUses SQLite for data persistence. Use the tabs to navigate.")

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg='#e0e0e0', bd=1, relief=tk.RAISED)

        # Logo
        logo_label = tk.Label(self.toolbar, text="📚 Student Dashboard", font=("Arial", 16, "bold"), bg='#e0e0e0', fg='#333')
        logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Separator
        separator = tk.Frame(self.toolbar, bg='#999', width=2, height=20)
        separator.pack(side=tk.LEFT, padx=10, pady=5)

        ttk.Button(self.toolbar, text="Refresh", command=self.display_students).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Save Data", command=self.save_data).pack(side=tk.LEFT, padx=5)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.add_tab = ttk.Frame(self.tab_control)
        self.display_tab = ttk.Frame(self.tab_control)
        self.search_tab = ttk.Frame(self.tab_control)
        self.edit_tab = ttk.Frame(self.tab_control)
        self.stats_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.add_tab, text='Add Student')
        self.tab_control.add(self.display_tab, text='Display Students')
        self.tab_control.add(self.search_tab, text='Search Student')
        self.tab_control.add(self.edit_tab, text='Edit/Delete Student')
        self.tab_control.add(self.stats_tab, text='Statistics')

        self.create_add_tab()
        self.create_display_tab()
        self.create_search_tab()
        self.create_edit_tab()
        self.create_statistics_tab()

    def create_add_tab(self):
        tab = self.add_tab

        # Title with icon
        title_frame = tk.Frame(tab, bg='#e8f4f8')
        title_frame.pack(fill="x", pady=10)
        title_label = tk.Label(title_frame, text="👨‍🎓 Add New Student", font=("Arial", 24, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)

        # Main container
        main_frame = tk.Frame(tab, bg='#f8f9fa')
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Personal Information Section
        personal_frame = tk.LabelFrame(main_frame, text="📋 Personal Information", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        personal_frame.pack(fill="x", pady=10, padx=10)

        # Configure grid weights
        personal_frame.columnconfigure(1, weight=1)

        # Name
        ttk.Label(personal_frame, text="Full Name:").grid(row=0, column=0, sticky="w", pady=8, padx=10)
        self.name_entry = ttk.Entry(personal_frame, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")
        self.name_entry.insert(0, "Enter full name")
        self.name_entry.config(foreground='grey')

        # Roll Number
        ttk.Label(personal_frame, text="Roll Number:").grid(row=1, column=0, sticky="w", pady=8, padx=10)
        self.roll_entry = ttk.Entry(personal_frame, font=("Arial", 10))
        self.roll_entry.grid(row=1, column=1, pady=8, padx=10, sticky="ew")

        # Age and Gender in same row
        age_gender_frame = tk.Frame(personal_frame)
        age_gender_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=8, padx=10)

        ttk.Label(age_gender_frame, text="Age:").pack(side="left", padx=(0, 5))
        self.age_entry = ttk.Entry(age_gender_frame, font=("Arial", 10), width=10)
        self.age_entry.pack(side="left", padx=5)

        ttk.Label(age_gender_frame, text="Gender:").pack(side="left", padx=(20, 5))
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(age_gender_frame, textvariable=self.gender_var,
                                         values=["Male", "Female", "Other"], state="readonly", width=10)
        self.gender_combo.pack(side="left", padx=5)

        # Academic Information Section
        academic_frame = tk.LabelFrame(main_frame, text="📚 Academic Performance", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        academic_frame.pack(fill="x", pady=10, padx=10)

        # Configure grid
        academic_frame.columnconfigure(1, weight=1)
        academic_frame.columnconfigure(3, weight=1)

        self.marks_entries = {}
        subjects = SUBJECTS
        for i, subject in enumerate(subjects):
            col = 0 if i < 3 else 2
            row = i % 3
            ttk.Label(academic_frame, text=f"{subject} (0-100):").grid(row=row, column=col, sticky="w", pady=5, padx=10)
            entry = ttk.Entry(academic_frame, font=("Arial", 10), width=15)
            entry.grid(row=row, column=col+1, pady=5, padx=10, sticky="w")
            self.marks_entries[subject.lower()] = entry

        # Action Buttons Section
        action_frame = tk.Frame(main_frame, bg='#f8f9fa')
        action_frame.pack(fill="x", pady=20, padx=10)

        # Buttons with better styling
        self.add_button = ttk.Button(action_frame, text="✅ Add Student", command=self.add_student, width=15)
        self.add_button.pack(side="left", padx=10)

        self.clear_button = ttk.Button(action_frame, text="🗑️ Clear Form", command=self.clear_add_form, width=15)
        self.clear_button.pack(side="left", padx=10)

        # Status display
        self.status_label = ttk.Label(action_frame, text="", foreground="blue")
        self.status_label.pack(side="right", padx=10)

        # Bind focus events for placeholders
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.name_entry, "Enter full name"))
        self.name_entry.bind("<FocusOut>", lambda e: self.set_placeholder(self.name_entry, "Enter full name"))

    def create_display_tab(self):
        tab = self.display_tab

        # Title with icon
        title_frame = tk.Frame(tab, bg='#e8f4f8')
        title_frame.pack(fill="x", pady=10)
        title_label = tk.Label(title_frame, text="📊 Display All Students", font=("Arial", 24, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)

        # Summary frame
        summary_frame = tk.Frame(tab, bg='#f8f9fa')
        summary_frame.pack(fill="x", pady=5, padx=10)
        self.summary_label = tk.Label(summary_frame, text="", font=("Arial", 12), bg='#f8f9fa', fg='#34495e')
        self.summary_label.pack(pady=5)

        # Controls frame
        controls_frame = tk.Frame(tab, bg='#f8f9fa')
        controls_frame.pack(fill="x", pady=5, padx=10)

        tk.Label(controls_frame, text="Filter by Grade:", bg='#f8f9fa').pack(side="left", padx=5)
        self.grade_filter_var = tk.StringVar(value="All")
        grade_combo = ttk.Combobox(controls_frame, textvariable=self.grade_filter_var, values=["All", "A", "B", "C", "D", "F"], state="readonly", width=5)
        grade_combo.pack(side="left", padx=5)
        grade_combo.bind("<<ComboboxSelected>>", lambda e: self.display_students())

        tk.Label(controls_frame, text="Filter by Gender:", bg='#f8f9fa').pack(side="left", padx=10)
        self.gender_filter_var = tk.StringVar(value="All")
        gender_combo = ttk.Combobox(controls_frame, textvariable=self.gender_filter_var, values=["All", "M", "F", "O"], state="readonly", width=5)
        gender_combo.pack(side="left", padx=5)
        gender_combo.bind("<<ComboboxSelected>>", lambda e: self.display_students())

        ttk.Button(controls_frame, text="Refresh", command=self.display_students).pack(side="right", padx=5)

        # Create Treeview with more columns
        columns = ('Name', 'Roll No', 'Age', 'Gender', 'Total', 'Percentage', 'Grade')
        self.display_tree = ttk.Treeview(tab, columns=columns, show='headings', height=15)
        for col in columns:
            self.display_tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            if col == 'Name':
                self.display_tree.column(col, width=150)
            elif col == 'Roll No':
                self.display_tree.column(col, width=80)
            elif col == 'Age':
                self.display_tree.column(col, width=50)
            elif col == 'Gender':
                self.display_tree.column(col, width=60)
            elif col == 'Total':
                self.display_tree.column(col, width=70)
            elif col == 'Percentage':
                self.display_tree.column(col, width=90)
            elif col == 'Grade':
                self.display_tree.column(col, width=50)

        # Configure tags for grade-based coloring
        self.display_tree.tag_configure('A', background='lightgreen')
        self.display_tree.tag_configure('B', background='yellow')
        self.display_tree.tag_configure('C', background='orange')
        self.display_tree.tag_configure('D', background='red')
        self.display_tree.tag_configure('F', background='gray')

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(tab, orient="vertical", command=self.display_tree.yview)
        scrollbar_x = ttk.Scrollbar(tab, orient="horizontal", command=self.display_tree.xview)
        self.display_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.display_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

    def create_search_tab(self):
        tab = self.search_tab

        # Title with icon
        title_frame = tk.Frame(tab, bg='#e8f4f8')
        title_frame.pack(fill="x", pady=10)
        title_label = tk.Label(title_frame, text="🔍 Search Student", font=("Arial", 24, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)

        # Search frame
        search_frame = tk.Frame(tab, bg='#f8f9fa')
        search_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(search_frame, text="Roll Number:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(search_frame, text="🔍 Search", command=self.search_student).pack(side="left", padx=5)
        ttk.Button(search_frame, text="🗑️ Clear", command=self.clear_search).pack(side="left", padx=5)

        # Results frame
        results_frame = tk.Frame(tab, bg='#f8f9fa')
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ttk.Label(results_frame, text="Search Results:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        self.search_result = tk.Text(results_frame, wrap="word", font=("Arial", 10), bg='white', fg='black')
        scrollbar = ttk.Scrollbar(results_frame, command=self.search_result.yview)
        self.search_result.config(yscrollcommand=scrollbar.set)

        self.search_result.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_edit_tab(self):
        tab = self.edit_tab

        # Title with icon
        title_frame = tk.Frame(tab, bg='#e8f4f8')
        title_frame.pack(fill="x", pady=10)
        title_label = tk.Label(title_frame, text="✏️ Edit or Delete Student", font=("Arial", 24, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)

        # Main container
        main_frame = tk.Frame(tab, bg='#f8f9fa')
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Search Section
        search_frame = tk.LabelFrame(main_frame, text="🔍 Find Student", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        search_frame.pack(fill="x", pady=10, padx=10)
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Roll Number:").grid(row=0, column=0, sticky="w", pady=8, padx=10)
        self.edit_roll_entry = ttk.Entry(search_frame, font=("Arial", 10))
        self.edit_roll_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")

        button_frame = tk.Frame(search_frame, bg='#f8f9fa')
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="📥 Load for Edit", command=self.load_student_for_edit).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Student", command=self.delete_student).pack(side="left", padx=5)

        # Edit form (initially hidden)
        self.edit_frame = tk.LabelFrame(main_frame, text="📝 Edit Student Details", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        self.edit_frame.pack(fill="x", pady=10, padx=10)

        # Personal Information
        personal_frame = tk.Frame(self.edit_frame, bg='#f8f9fa')
        personal_frame.pack(fill="x", pady=5, padx=10)
        personal_frame.columnconfigure(1, weight=1)

        ttk.Label(personal_frame, text="Full Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.edit_name_entry = ttk.Entry(personal_frame, font=("Arial", 10))
        self.edit_name_entry.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        ttk.Label(personal_frame, text="Age:").grid(row=1, column=0, sticky="w", pady=5)
        self.edit_age_entry = ttk.Entry(personal_frame, font=("Arial", 10))
        self.edit_age_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        ttk.Label(personal_frame, text="Gender (M/F/O):").grid(row=2, column=0, sticky="w", pady=5)
        self.edit_gender_entry = ttk.Entry(personal_frame, font=("Arial", 10))
        self.edit_gender_entry.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        # Academic Information
        marks_frame = tk.LabelFrame(self.edit_frame, text="📚 Academic Performance", font=("Arial", 10, "bold"), bg='#f8f9fa', fg='#34495e')
        marks_frame.pack(fill="x", pady=10, padx=10)
        marks_frame.columnconfigure(1, weight=1)
        marks_frame.columnconfigure(3, weight=1)

        self.edit_marks_entries = {}
        for i, subject in enumerate(SUBJECTS):
            col = 0 if i < 3 else 2
            row = i % 3
            ttk.Label(marks_frame, text=f"{subject} (0-100):").grid(row=row, column=col, sticky="w", pady=5, padx=10)
            entry = ttk.Entry(marks_frame, font=("Arial", 10), width=15)
            entry.grid(row=row, column=col+1, pady=5, padx=10, sticky="w")
            self.edit_marks_entries[subject.lower()] = entry

        # Action Buttons
        action_frame = tk.Frame(self.edit_frame, bg='#f8f9fa')
        action_frame.pack(fill="x", pady=20, padx=10)
        ttk.Button(action_frame, text="✅ Update Student", command=self.update_student).pack(side="left", padx=10)
        ttk.Button(action_frame, text="🗑️ Clear Form", command=self.clear_edit_form).pack(side="left", padx=10)

        # Status display
        self.edit_status_label = ttk.Label(action_frame, text="", foreground="blue")
        self.edit_status_label.pack(side="right", padx=10)

        # Initially hide the edit frame
        self.edit_frame.pack_forget()

    def create_statistics_tab(self):
        tab = self.stats_tab

        # Title with icon
        title_frame = tk.Frame(tab, bg='#e8f4f8')
        title_frame.pack(fill="x", pady=10)
        title_label = tk.Label(title_frame, text="📊 Class Statistics", font=("Arial", 24, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title_label.pack(pady=10)

        # Main container
        main_frame = tk.Frame(tab, bg='#f8f9fa')
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Controls frame
        controls_frame = tk.Frame(main_frame, bg='#f8f9fa')
        controls_frame.pack(fill="x", pady=10, padx=10)

        ttk.Button(controls_frame, text="📈 Show Statistics", command=self.show_statistics).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="📤 Export CSV", command=self.export_csv).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="📥 Import CSV", command=self.import_csv).pack(side="left", padx=5)

        # Statistics display
        stats_container = tk.Frame(main_frame, bg='#f8f9fa')
        stats_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Overall Statistics Frame
        overall_frame = tk.LabelFrame(stats_container, text="📊 Overall Statistics", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        overall_frame.pack(fill="x", pady=5)
        overall_frame.columnconfigure(1, weight=1)

        self.total_label = tk.Label(overall_frame, text="", font=("Arial", 11), bg='#f8f9fa', fg='#2c3e50')
        self.total_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.avg_age_label = tk.Label(overall_frame, text="", font=("Arial", 11), bg='#f8f9fa', fg='#2c3e50')
        self.avg_age_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.highest_scorer_label = tk.Label(overall_frame, text="", font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#27ae60')
        self.highest_scorer_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Class Average
        self.class_avg_label = tk.Label(overall_frame, text="", font=("Arial", 11, "bold"), bg='#f8f9fa', fg='#3498db')
        self.class_avg_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Grade Distribution Treeview
        grade_frame = tk.LabelFrame(stats_container, text="📈 Grade Distribution", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        grade_frame.pack(fill="x", pady=5)

        grade_columns = ('Grade', 'Count', 'Percentage')
        self.grade_tree = ttk.Treeview(grade_frame, columns=grade_columns, show='headings', height=6)
        for col in grade_columns:
            self.grade_tree.heading(col, text=col)
            if col == 'Grade':
                self.grade_tree.column(col, width=80)
            elif col == 'Count':
                self.grade_tree.column(col, width=80)
            else:
                self.grade_tree.column(col, width=100)
        grade_scrollbar = ttk.Scrollbar(grade_frame, orient="vertical", command=self.grade_tree.yview)
        self.grade_tree.configure(yscrollcommand=grade_scrollbar.set)
        self.grade_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        grade_scrollbar.pack(side="right", fill="y")

        # Gender Distribution Treeview
        gender_frame = tk.LabelFrame(stats_container, text="👥 Gender Distribution", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        gender_frame.pack(fill="x", pady=5)

        gender_columns = ('Gender', 'Count', 'Percentage')
        self.gender_tree = ttk.Treeview(gender_frame, columns=gender_columns, show='headings', height=4)
        for col in gender_columns:
            self.gender_tree.heading(col, text=col)
            if col == 'Gender':
                self.gender_tree.column(col, width=100)
            elif col == 'Count':
                self.gender_tree.column(col, width=80)
            else:
                self.gender_tree.column(col, width=100)
        gender_scrollbar = ttk.Scrollbar(gender_frame, orient="vertical", command=self.gender_tree.yview)
        self.gender_tree.configure(yscrollcommand=gender_scrollbar.set)
        self.gender_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        gender_scrollbar.pack(side="right", fill="y")

        # Subject Averages Treeview
        subject_frame = tk.LabelFrame(stats_container, text="📚 Subject Averages", font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#34495e')
        subject_frame.pack(fill="x", pady=5)

        subject_columns = ('Subject', 'Average')
        self.subject_tree = ttk.Treeview(subject_frame, columns=subject_columns, show='headings', height=6)
        for col in subject_columns:
            self.subject_tree.heading(col, text=col)
            if col == 'Subject':
                self.subject_tree.column(col, width=150)
            else:
                self.subject_tree.column(col, width=100)
        subject_scrollbar = ttk.Scrollbar(subject_frame, orient="vertical", command=self.subject_tree.yview)
        self.subject_tree.configure(yscrollcommand=subject_scrollbar.set)
        self.subject_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        subject_scrollbar.pack(side="right", fill="y")

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text=f"Total Students: {len(self.students)}", bd=1, relief=tk.SUNKEN, anchor=tk.W)

    def add_student(self):
        try:
            name_input = self.name_entry.get().strip()
            if name_input == "Enter full name":
                raise ValueError("Please enter a valid name")
            name = validate_name(name_input)
            roll_no = int(self.roll_entry.get())
            age = int(self.age_entry.get())
            gender_input = self.gender_var.get()
            if not gender_input:
                raise ValueError("Please select a gender")
            if gender_input == "Male":
                gender = 'M'
            elif gender_input == "Female":
                gender = 'F'
            elif gender_input == "Other":
                gender = 'O'
            else:
                raise ValueError("Invalid gender selection")
            marks = []
            for subject in SUBJECTS:
                mark_str = self.marks_entries[subject.lower()].get().strip()
                if not mark_str:
                    raise ValueError(f"Please enter marks for {subject}")
                mark = float(mark_str)
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
            self.manager.add_student(student)
            self.students = self.manager.get_all_students()
            self.status_label.config(text="Student added successfully!", foreground="green")
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            self.clear_add_form()
            self.display_students()
            self.update_status()
        except ValueError as e:
            self.status_label.config(text=str(e), foreground="red")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_label.config(text="Unexpected error occurred", foreground="red")
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def display_students(self):
        self.students = self.manager.get_all_students()
        # Clear the treeview
        for item in self.display_tree.get_children():
            self.display_tree.delete(item)

        # Apply filters
        grade_filter = self.grade_filter_var.get()
        gender_filter = self.gender_filter_var.get()
        filtered_students = [
            s for s in self.students
            if (grade_filter == "All" or s['grade'] == grade_filter) and
               (gender_filter == "All" or s['gender'] == gender_filter)
        ]

        # Update summary
        total_students = len(filtered_students)
        avg_percentage = sum(s['percentage'] for s in filtered_students) / total_students if total_students > 0 else 0
        self.summary_label.config(text=f"Showing {total_students} students | Average Percentage: {avg_percentage:.2f}%")

        if not filtered_students:
            # Insert a placeholder row
            self.display_tree.insert('', 'end', values=('No students to display.', '', '', '', '', '', ''))
            return

        for student in filtered_students:
            self.display_tree.insert('', 'end', values=(
                student['name'],
                student['roll_no'],
                student['age'],
                student['gender'],
                student['total'],
                f"{student['percentage']:.2f}",
                student['grade']
            ), tags=(student['grade'],))

    def search_student(self):
        self.search_result.delete(1.0, tk.END)
        try:
            roll_no = int(self.search_entry.get())
            student = self.manager.get_student(roll_no)
            if student:
                self.search_result.insert(tk.END, f"Name: {student['name']}\n")
                self.search_result.insert(tk.END, f"Age: {student['age']}\n")
                self.search_result.insert(tk.END, f"Gender: {student['gender']}\n")
                self.search_result.insert(tk.END, f"Marks:\n")
                for subject, mark in zip(SUBJECTS, student['marks']):
                    self.search_result.insert(tk.END, f"  {subject}: {mark}\n")
                self.search_result.insert(tk.END, f"Total: {student['total']}\n")
                self.search_result.insert(tk.END, f"Percentage: {student['percentage']:.2f}%\n")
                self.search_result.insert(tk.END, f"Grade: {student['grade']}\n")
            else:
                messagebox.showinfo("Not Found", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number.")

    def show_statistics(self):
        self.students = self.manager.get_all_students()
        if not self.students:
            self.total_label.config(text="No data available.")
            self.avg_age_label.config(text="")
            self.highest_scorer_label.config(text="")
            self.class_avg_label.config(text="")
            # Clear treeviews
            for tree in [self.grade_tree, self.gender_tree, self.subject_tree]:
                for item in tree.get_children():
                    tree.delete(item)
            return

        total_students = len(self.students)

        # Overall Statistics
        self.total_label.config(text=f"Total Students: {total_students}")

        # Average Age
        avg_age = sum(s['age'] for s in self.students) / total_students
        self.avg_age_label.config(text=f"Average Age: {avg_age:.1f} years")

        # Highest Scorer
        highest = self.manager.find_highest_scorer()
        if highest:
            self.highest_scorer_label.config(text=f"🏆 Highest Scorer: {highest['name']} with {highest['total']} marks")
        else:
            self.highest_scorer_label.config(text="No students available.")

        # Class Average Percentage
        avg_percentage = sum(s['percentage'] for s in self.students) / total_students
        self.class_avg_label.config(text=f"📉 Class Average Percentage: {avg_percentage:.2f}%")

        # Clear treeviews
        for tree in [self.grade_tree, self.gender_tree, self.subject_tree]:
            for item in tree.get_children():
                tree.delete(item)

        # Grade Distribution
        from collections import Counter
        grades = [s['grade'] for s in self.students]
        grade_counts = Counter(grades)
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = grade_counts.get(grade, 0)
            percentage = (count / total_students) * 100 if total_students > 0 else 0
            self.grade_tree.insert('', 'end', values=(grade, count, f"{percentage:.1f}%"))

        # Gender Distribution
        genders = [s['gender'] for s in self.students]
        gender_counts = Counter(genders)
        gender_map = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
        for g, label in gender_map.items():
            count = gender_counts.get(g, 0)
            percentage = (count / total_students) * 100 if total_students > 0 else 0
            self.gender_tree.insert('', 'end', values=(label, count, f"{percentage:.1f}%"))

        # Subject Averages
        averages = self.manager.calculate_subject_averages()
        for subject, avg in zip(SUBJECTS, averages):
            self.subject_tree.insert('', 'end', values=(subject, f"{avg:.2f}"))

    def clear_add_form(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, "Enter full name")
        self.name_entry.config(foreground='grey')
        self.roll_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.gender_combo.set("")
        for entry in self.marks_entries.values():
            entry.delete(0, tk.END)
        self.status_label.config(text="")

    def save_data(self):
        # Data is automatically saved via SQLite
        messagebox.showinfo("Success", "Data is persisted in SQLite database.")

    def export_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            import json
            with open(file_path, 'w') as f:
                json.dump(self.students, f, indent=4, default=str)
            messagebox.showinfo("Success", "Data exported successfully!")

    def import_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                import json
                with open(file_path, 'r') as f:
                    imported_students = json.load(f)
                # Clear existing and add imported
                self.manager.delete_all_students()  # Careful: this deletes all
                for student in imported_students:
                    self.manager.add_student(student)
                self.students = self.manager.get_all_students()
                self.display_students()
                self.update_status()
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.manager.export_csv(file_path)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.manager.import_csv(file_path)
                self.students = self.manager.get_all_students()
                self.display_students()
                self.update_status()
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")

    def update_status(self):
        self.status_bar.config(text=f"Total Students: {len(self.students)}")

    def load_student_for_edit(self):
        try:
            roll_no = int(self.edit_roll_entry.get())
            student = self.manager.get_student(roll_no)
            if student:
                self.edit_name_entry.delete(0, tk.END)
                self.edit_name_entry.insert(0, student['name'])
                self.edit_age_entry.delete(0, tk.END)
                self.edit_age_entry.insert(0, str(student['age']))
                self.edit_gender_entry.delete(0, tk.END)
                self.edit_gender_entry.insert(0, student['gender'])
                for i, subject in enumerate(SUBJECTS):
                    self.edit_marks_entries[subject.lower()].delete(0, tk.END)
                    self.edit_marks_entries[subject.lower()].insert(0, str(student['marks'][i]))
                self.edit_frame.pack()
                self.edit_status_label.config(text="Student loaded successfully!", foreground="green")
            else:
                messagebox.showinfo("Not Found", "Student not found.")
                self.edit_frame.pack_forget()
                self.edit_status_label.config(text="Student not found.", foreground="red")
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number.")
            self.edit_status_label.config(text="Invalid roll number.", foreground="red")

    def update_student(self):
        try:
            roll_no = int(self.edit_roll_entry.get())
            name = validate_name(self.edit_name_entry.get())
            age = int(self.edit_age_entry.get())
            gender = self.edit_gender_entry.get().upper()
            if gender not in ['M', 'F', 'O']:
                raise ValueError("Gender must be M, F, or O")
            marks = []
            for subject in SUBJECTS:
                mark = float(self.edit_marks_entries[subject.lower()].get())
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
            if self.manager.update_student(roll_no, updated_fields):
                self.edit_status_label.config(text=f"Student {name} updated successfully!", foreground="green")
                messagebox.showinfo("Success", f"Student {name} updated successfully!")
                self.clear_edit_form()
                self.display_students()
                self.update_status()
            else:
                self.edit_status_label.config(text="Failed to update student.", foreground="red")
                messagebox.showerror("Error", "Failed to update student.")
        except ValueError as e:
            self.edit_status_label.config(text=str(e), foreground="red")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.edit_status_label.config(text="Unexpected error occurred", foreground="red")
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def delete_student(self):
        try:
            roll_no = int(self.edit_roll_entry.get())
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with roll number {roll_no}?"):
                if self.manager.delete_student(roll_no):
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    self.clear_edit_form()
                    self.display_students()
                    self.update_status()
                else:
                    messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number.")

    def clear_edit_form(self):
        self.edit_roll_entry.delete(0, tk.END)
        self.edit_name_entry.delete(0, tk.END)
        self.edit_age_entry.delete(0, tk.END)
        self.edit_gender_entry.delete(0, tk.END)
        for entry in self.edit_marks_entries.values():
            entry.delete(0, tk.END)
        self.edit_frame.pack_forget()

    def clear_placeholder(self, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def set_placeholder(self, entry, placeholder_text):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey')

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search_result.delete(1.0, tk.END)

    def sort_treeview(self, col):
        # Get all items
        items = [(self.display_tree.set(item, col), item) for item in self.display_tree.get_children('')]

        # Sort items
        try:
            items.sort(key=lambda t: float(t[0]) if t[0].replace('.', '').isdigit() else t[0])
        except ValueError:
            items.sort(key=lambda t: t[0])

        # Rearrange items in sorted positions
        for index, (val, item) in enumerate(items):
            self.display_tree.move(item, '', index)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StudentDashboardApp()
    app.run()
