"""Command-line interface for the gradebook."""

import argparse
from gradebook import service
from gradebook.storage import load_data, save_data, get_logger


def build_parser():
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(description="A simple student gradebook.")
    commands = parser.add_subparsers(dest="command", required=True)

    student = commands.add_parser("add-student", help="Add a student")
    student.add_argument("--name", required=True)

    course = commands.add_parser("add-course", help="Add a course")
    course.add_argument("--code", required=True)
    course.add_argument("--title", required=True)

    enrollment = commands.add_parser("enroll", help="Enroll a student")
    enrollment.add_argument("--student-id", type=int, required=True)
    enrollment.add_argument("--course", required=True)

    grade = commands.add_parser("add-grade", help="Add a grade")
    grade.add_argument("--student-id", type=int, required=True)
    grade.add_argument("--course", required=True)
    grade.add_argument("--grade", required=True)

    listing = commands.add_parser("list", help="List gradebook records")
    listing.add_argument("kind", choices=("students", "courses", "enrollments"))
    listing.add_argument("--sort", choices=("name", "code"))

    average = commands.add_parser("avg", help="Show a course average")
    average.add_argument("--student-id", type=int, required=True)
    average.add_argument("--course", required=True)

    gpa = commands.add_parser("gpa", help="Show a student's GPA")
    gpa.add_argument("--student-id", type=int, required=True)
    return parser


def show_list(data, args):
    """Print the requested list in a readable format."""
    if args.kind == "students":
        records = service.list_students(data, args.sort or "name")
        for item in records:
            print(f'{item["id"]}: {item["name"]}')
    elif args.kind == "courses":
        records = service.list_courses(data, args.sort or "code")
        for item in records:
            print(f'{item["code"]}: {item["title"]}')
    else:
        records = service.list_enrollments(data)
        for item in records:
            grades = ", ".join(f"{grade:g}" for grade in item["grades"]) or "none"
            print(
                f'Student {item["student_id"]} - {item["course_code"]}: '
                f'grades {grades}'
            )
    if not records:
        print("No records found.")


def main():
    """Run the CLI command and handle expected application errors."""
    parser = build_parser()
    args = parser.parse_args()
    logger = get_logger()
    try:
        data = load_data()
        if args.command == "add-student":
            data, student_id = service.add_student(data, args.name)
            save_data(data)
            print(f"Student added successfully. ID: {student_id}")
        elif args.command == "add-course":
            data = service.add_course(data, args.code, args.title)
            save_data(data)
            print(f"Course {args.code.strip().upper()} added successfully.")
        elif args.command == "enroll":
            data = service.enroll(data, args.student_id, args.course)
            save_data(data)
            print("Student enrolled successfully.")
        elif args.command == "add-grade":
            grade = service.parse_grade(args.grade)
            data = service.add_grade(data, args.student_id, args.course, grade)
            save_data(data)
            print("Grade added successfully.")
        elif args.command == "list":
            show_list(data, args)
        elif args.command == "avg":
            result = service.compute_average(data, args.student_id, args.course)
            print(f"Average: {result:.2f}")
        elif args.command == "gpa":
            result = service.compute_gpa(data, args.student_id)
            print(f"GPA: {result:.2f}")
    except (ValueError, OSError) as error:
        logger.error("Command '%s' failed: %s", args.command, error)
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
