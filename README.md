# Gradebook CLI

This is a simple Python project to manage students, courses and their marks. It runs in the terminal and saves all the data in a JSON file.

## Setup

First, open the project folder in the terminal and create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

No extra libraries are needed.

## Add sample data

Run:

```bash
python scripts/seed.py
```

This will add 3 students, 3 courses and some sample marks to the gradebook.

## Running the project

Add a student:

```bash
python main.py add-student --name "Riya Mehta"
```

Add a course:

```bash
python main.py add-course --code CS201 --title "Data Structures"
```

Enroll a student and add marks:

```bash
python main.py enroll --student-id 4 --course CS201
python main.py add-grade --student-id 4 --course CS201 --grade 95
```

Show students, courses and enrollments:

```bash
python main.py list students
python main.py list courses
python main.py list enrollments
```

Find the average and GPA:

```bash
python main.py avg --student-id 1 --course CS101
python main.py gpa --student-id 1
```

For the sample data, the output is:

```text
Average: 90.00
GPA: 92.50
```

The program also shows an error message if an invalid grade is entered or a student or course is not found.


## Design decisions & limitations

- I used JSON to store the data instead of a database.
- Each student gets a unique ID.
- The GPA is calculated by taking the average of all course averages.
- Grades must be between 0 and 100.
- The project is made for basic use. It does not support multiple users working on it at the same time.

## Running tests

Run this command:

```bash
python -m unittest discover -s tests -v
```
