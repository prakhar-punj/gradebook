"""Put some sample data in the gradebook."""

import sys
from pathlib import Path

# This lets the script find the gradebook folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gradebook import service
from gradebook.storage import empty_data, save_data


def main():
    """Create sample students and courses."""
    data = empty_data()

    data, prakhar = service.add_student(data, "Prakhar Punj")
    data, riya = service.add_student(data, "Riya Sharma")
    data, arjun = service.add_student(data, "Arjun Reddy")

    data = service.add_course(data, "CS101", "Intro to CS")
    data = service.add_course(data, "DA201", "Data Analysis")
    data = service.add_course(data, "GEN101", "Genpact Python Basics")

    data = service.enroll(data, prakhar, "CS101")
    data = service.enroll(data, prakhar, "DA201")
    data = service.enroll(data, riya, "CS101")
    data = service.enroll(data, riya, "GEN101")
    data = service.enroll(data, arjun, "CS101")

    data = service.add_grade(data, prakhar, "CS101", 92)
    data = service.add_grade(data, prakhar, "CS101", 88)
    data = service.add_grade(data, prakhar, "DA201", 95)
    data = service.add_grade(data, riya, "CS101", 81)
    data = service.add_grade(data, riya, "GEN101", 79)
    data = service.add_grade(data, arjun, "CS101", 90)

    save_data(data)
    print("Sample data saved to data/gradebook.json")


if __name__ == "__main__":
    main()
