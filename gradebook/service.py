"""Functions used in the gradebook."""

from copy import deepcopy

from .models import Student, Course, Enrollment


def parse_grade(value):
    """Check if the grade is valid."""
    try:
        marks = float(value)
    except (TypeError, ValueError):
        raise ValueError("Grade should be between 0 and 100.")

    if marks < 0 or marks > 100:
        raise ValueError("Grade should be between 0 and 100.")

    return marks


def add_student(data, name):
    """Add a new student."""
    data = deepcopy(data)

    sid = max([s["id"] for s in data["students"]], default=0) + 1
    student = Student(sid, name)

    data["students"].append({
        "id": sid,
        "name": student.name
    })

    return data, sid


def add_course(data, code, title):
    """Add a new course."""
    data = deepcopy(data)
    course = Course(code, title)

    for c in data["courses"]:
        if c["code"] == course.code:
            raise ValueError("Course already exists.")

    data["courses"].append({
        "code": course.code,
        "title": course.title
    })

    return data


def enroll(data, student_id, course_code):
    """Enroll a student in a course."""
    data = deepcopy(data)
    code = course_code.strip().upper()

    # Check if the student and course are present.
    found_student = False
    found_course = False

    for s in data["students"]:
        if s["id"] == student_id:
            found_student = True

    for c in data["courses"]:
        if c["code"] == code:
            found_course = True

    if not found_student:
        raise ValueError("Student ID not found.")

    if not found_course:
        raise ValueError("Course not found.")

    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == code:
            raise ValueError("Student is already enrolled.")

    new_entry = Enrollment(student_id, code)

    data["enrollments"].append({
        "student_id": student_id,
        "course_code": code,
        "grades": new_entry.grades
    })

    return data


def add_grade(data, student_id, course_code, grade):
    """Add marks for a student."""
    data = deepcopy(data)
    marks = parse_grade(grade)
    code = course_code.strip().upper()

    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == code:
            record = Enrollment(student_id, code, e["grades"])
            record.add_grade(marks)
            e["grades"] = record.grades
            return data

    raise ValueError("Student is not enrolled in this course.")


def list_students(data, sort_by="name"):
    """Get the list of students."""
    if sort_by == "name":
        return sorted(data["students"], key=lambda s: s["name"].lower())

    return sorted(data["students"], key=lambda s: s["id"])


def list_courses(data, sort_by="code"):
    """Get the list of courses."""
    if sort_by == "name":
        return sorted(data["courses"], key=lambda c: c["title"].lower())

    return sorted(data["courses"], key=lambda c: c["code"])


def list_enrollments(data):
    """Get all enrollments."""
    return sorted(
        data["enrollments"],
        key=lambda e: (e["student_id"], e["course_code"])
    )


def compute_average(data, student_id, course_code):
    """Calculate the average marks for a course."""
    code = course_code.strip().upper()

    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == code:
            if len(e["grades"]) == 0:
                raise ValueError("No grades added yet.")

            return sum(e["grades"]) / len(e["grades"])

    raise ValueError("Student is not enrolled in this course.")


def compute_gpa(data, student_id):
    """Calculate the average of all course averages."""
    exists = False

    for s in data["students"]:
        if s["id"] == student_id:
            exists = True

    if not exists:
        raise ValueError("Student ID not found.")

    course_avgs = []

    for e in data["enrollments"]:
        if e["student_id"] == student_id and len(e["grades"]) > 0:
            avg = sum(e["grades"]) / len(e["grades"])
            course_avgs.append(avg)

    if len(course_avgs) == 0:
        raise ValueError("No grades found for this student.")

    return sum(course_avgs) / len(course_avgs)