# 🎓 Student Performance Management System

A comprehensive Python application for managing student performance data with Command Line Interface (CLI), Graphical User Interface (GUI), and Web App implementations. Now featuring SQLite database for efficient data management, edit/delete functionality, logging, type hints, and unit tests.

## 📋 Features

### ✨ Core Functionality

- **Student Data Management**: Add, view, search, and delete student records
- **Performance Calculation**: Automatic calculation of total marks, percentage, and grade assignment
- **Data Persistence**: Save and load data using JSON format
- **Statistics & Analytics**: Class performance statistics, subject-wise averages, grade distribution
- **Dual Interface**: Both CLI and GUI versions available

### 🎯 Python Concepts Implemented

#### **Setup & Basics**

- ✅ Print welcome messages with proper formatting
- ✅ Comprehensive comments throughout the codebase
- ✅ Modular file structure for better organization

#### **Variables, Input/Output, Operators**

- ✅ Student data collection (Name, Roll No, Age, Gender)
- ✅ Marks input for 5 subjects
- ✅ Mathematical operations for total and percentage calculation
- ✅ String manipulation and formatting

#### **Control Flow**

- ✅ **If-else statements**: Grade assignment based on percentage
- ✅ **For loops**: Collecting marks for multiple subjects
- ✅ **While loops**: Menu navigation and input validation
- ✅ **Match-case**: Menu selection and grade assignment (Python 3.10+)
- ✅ **Break/Continue**: Input validation and menu flow control

#### **Functions & Scope**

- ✅ **calculate_percentage()**: Calculates student percentage
- ✅ **assign_grade()**: Assigns grades based on percentage
- ✅ **search_student()**: Search functionality by name/roll number
- ✅ **calculate_class_statistics()**: Comprehensive statistics calculation
- ✅ **factorial_recursive()**: Recursive function for roll number factorial
- ✅ Proper variable scope management and parameter passing

#### **Arrays/Lists & Data Structures**

- ✅ List of student records (multi-dimensional data)
- ✅ Subject marks stored as lists
- ✅ Dynamic data manipulation and sorting
- ✅ Statistical analysis on datasets

#### **String Manipulation**

- ✅ Name validation and formatting
- ✅ Input sanitization and case handling
- ✅ String slicing and length validation
- ✅ Pattern matching with regular expressions

#### **Exception Handling**

- ✅ Try/except blocks for input validation
- ✅ Division by zero protection
- ✅ File I/O error handling
- ✅ Type conversion error management
- ✅ Graceful error recovery

#### **GUI (Tkinter)**

- ✅ Complete GUI interface with multiple tabs
- ✅ Form validation and user feedback
- ✅ Data visualization in tables
- ✅ Interactive search functionality
- ✅ Statistics display with formatted text

## 📁 File Structure

```
student_dashboard/
├── main.py         # CLI application with menu-driven interface
├── gui.py          # GUI application using Tkinter
├── web_app.py      # Web application using Flask
├── helpers.py      # Utility functions and data operations
├── data.json       # Persistent data storage (auto-generated)
├── templates/      # HTML templates for the web app
│   ├── base.html
│   ├── home.html
│   ├── add_student.html
│   ├── display_students.html
│   ├── search_student.html
│   └── statistics.html
└── README.md       # Project documentation and usage guide
```

## 🚀 How to Run

### Prerequisites

- Python 3.7 or higher
- Tkinter (usually included with Python)

### Running the CLI Version

```bash
python main.py
```

### Running the GUI Version (Tkinter)

The GUI uses Tkinter, which opens a separate window. To run in VSCode with Code Runner:

1. Open `gui.py` in VSCode.
2. Ensure the Code Runner extension is installed (search "Code Runner" in Extensions and install if needed).
3. Configure VSCode settings:
   - Press Ctrl+, (or File > Preferences > Settings).
   - Search for "code-runner.runInTerminal".
   - Check the box for "Code-runner: Run In Terminal" (this runs the script in the integrated terminal, allowing the GUI window to appear).
4. Press Ctrl+Alt+N (or right-click in the editor > "Run Code").
   - The terminal will show output, and the GUI window should pop up separately.
5. If no window appears:
   - Ensure your system allows pop-ups/windows from VSCode.
   - Open the integrated terminal (Ctrl+`) and run: `python gui.py`.
   - Check for errors in the terminal output.

**Note**: Tkinter GUIs may not display directly in the VSCode output panel; they require a terminal run for the window to show.

Alternatively, run directly in terminal:
```bash
python gui.py
```

### Running the Web App Version (Local)

First, install dependencies:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python web_app.py
```

The web app will be available at http://localhost:5000

### Deploying to Heroku (Live URL)

To deploy the app to Heroku for a public URL:

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create your-app-name` (choose a unique name)
4. Add PostgreSQL (recommended over SQLite for production): `heroku addons:create heroku-postgresql:hobby-dev`
5. Set environment variables if needed (e.g., for DB config).
6. Git push: `git push heroku main`
7. Scale: `heroku ps:scale web=1`
8. Open: `heroku open`

The app will be live at https://your-app-name.herokuapp.com

**Note**: SQLite works locally but is read-only on Heroku. For full functionality, update database.py to use SQLAlchemy with PostgreSQL URI from `os.environ.get('DATABASE_URL')`.

For free hosting alternatives: Render.com or PythonAnywhere.

### Installation (if needed)

```bash
# Clone or download the project files
# For web app: pip install flask
# No additional packages required for CLI/GUI - uses only Python standard library
```

## 💡 Usage Guide

### CLI Interface Features:

1. **Add New Student**: Enter student details and marks
2. **Display All Students**: View summary of all students
3. **View Student Details**: Detailed view of individual student
4. **Search Students**: Find students by name or roll number
5. **Class Statistics**: Comprehensive performance analytics
6. **Save/Load Data**: Persistent data management
7. **Exit**: Save and close application

### GUI Interface Features:

- **Add Student Tab**: Form-based student data entry
- **View Students Tab**: Table view with edit/delete options
- **Search Tab**: Live search functionality
- **Statistics Tab**: Visual statistics display

## 🎯 Core Algorithms

### Grade Assignment Logic

```
A+ (90-100%) | A (80-89%) | B+ (70-79%) | B (60-69%) | C (50-59%) | D (40-49%) | F (<40%)
```

### Statistics Calculations

- Class average percentage
- Subject-wise averages
- Highest and lowest performers
- Grade distribution analysis

## 🧠 AI Usage (Development Process)

During development, AI tools were used as learning companions for:

### 🔍 **Research & Planning**

- Understanding Python best practices
- GUI design patterns with Tkinter
- Exception handling strategies

### 🐛 **Debugging Assistance**

- Identifying logic errors in recursive functions
- Troubleshooting GUI layout issues
- Fixing data validation edge cases

### ⚡ **Enhancement Ideas**

- Code optimization suggestions
- User experience improvements
- Advanced feature implementation

### 🎨 **Code Structure**

- Modular design recommendations
- Function organization and naming
- Documentation and commenting standards

_AI was used as a supportive tool while ensuring all core logic and implementation was understood and written with full comprehension._

## 🎨 Advanced Features

### 🔄 **Data Persistence**

- Automatic save on exit
- JSON format for human-readable storage
- Data integrity validation

### 📊 **Statistics Dashboard**

- Real-time calculation updates
- Visual grade distribution
- Performance trend analysis

### 🔍 **Smart Search**

- Case-insensitive name search
- Exact roll number matching
- Live search results in GUI

### 🛡️ **Input Validation**

- Comprehensive error checking
- User-friendly error messages
- Graceful failure recovery

## 🏆 Bonus Features Implemented

- ✅ **Search Bar in GUI**: Live search functionality
- ✅ **Save/Load Feature**: JSON-based data persistence
- ✅ **Class Average**: Comprehensive statistical analysis
- ✅ **Detailed Student View**: Individual performance analysis
- ✅ **Grade Distribution**: Visual representation of class performance
- ✅ **Roll Number Factorial**: Recursive function implementation
- ✅ **Data Export/Import**: Cross-session data continuity

## 🔧 Technical Implementation Details

### **Validation System**

- Name: Alphabets and spaces only
- Roll Number: Unique positive integers
- Age: Range validation (5-100)
- Marks: Integer validation (0-100)

### **Error Handling**

- Input type validation
- Duplicate roll number prevention
- File I/O exception management
- Graceful degradation on errors

### **Performance Optimizations**

- Efficient search algorithms
- Memory-conscious data structures
- Lazy loading for large datasets

## 🎓 Learning Outcomes

This project successfully demonstrates mastery of:

- **Core Python Programming**: Variables, operators, control flow
- **Object-Oriented Concepts**: Class design and method organization
- **Error Handling**: Robust exception management
- **GUI Development**: User-friendly interface design
- **Data Management**: File I/O and data persistence
- **Algorithm Implementation**: Search, sort, and statistical calculations
- **Software Architecture**: Modular design and code organization

## 📈 Future Enhancement Ideas

- Database integration (SQLite/PostgreSQL)
- Data visualization with matplotlib
- Export to Excel/PDF functionality
- Multi-class management
- Teacher/Admin role management
- Web interface development
- Mobile app version

---

**Author**: Student Performance Management System  
**Version**: 1.0.0  
**Python Version**: 3.7+  
**Last Updated**: 2024

_Happy Learning! 🚀_
