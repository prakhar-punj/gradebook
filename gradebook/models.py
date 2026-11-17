"""Classes for students, courses and enrollments."""


class Student:
    """A student in the gradebook."""

    def __init__(self, student_id, name):
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("Student ID must be a positive number.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")
        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"{self.id}: {self.name}"


class Course:
    """A course in the gradebook."""

    def __init__(self, code, title):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title cannot be empty.")
        self.code = code.strip().upper()
        self.title = title.strip()

    def __str__(self):
        return f"{self.code}: {self.title}"


class Enrollment:
    """A student's enrollment in a course."""

    def __init__(self, student_id, course_code, grades=None):
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("Student ID must be a positive number.")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code cannot be empty.")
        self.student_id = student_id
        self.course_code = course_code.strip().upper()
        self.grades = []

        for grade in grades or []:
            self.add_grade(grade)

    def add_grade(self, grade):
        """Add a grade after checking it."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError("Grade must be between 0 and 100.")
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100.")
        self.grades.append(float(grade))

    def __str__(self):
        return f"{self.student_id} - {self.course_code}: {self.grades}"
