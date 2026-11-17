"""Tests for the gradebook service."""

import unittest

from gradebook import service
from gradebook.storage import empty_data


class TestGradebook(unittest.TestCase):
    def setUp(self):
        self.data = empty_data()
        self.data, self.sid = service.add_student(self.data, "Prakhar Punj")
        self.data = service.add_course(self.data, "CS101", "Intro to CS")
        self.data = service.enroll(self.data, self.sid, "CS101")

    def test_add_student(self):
        data, sid = service.add_student(self.data, "Aarav Mehta")
        self.assertEqual(sid, 2)
        self.assertEqual(data["students"][1]["name"], "Aarav Mehta")

    def test_add_grade_and_average(self):
        data = service.add_grade(self.data, self.sid, "CS101", 80)
        data = service.add_grade(data, self.sid, "CS101", 100)
        self.assertEqual(service.compute_average(data, self.sid, "CS101"), 90)

    def test_wrong_grade(self):
        with self.assertRaises(ValueError):
            service.add_grade(self.data, self.sid, "CS101", 120)

    def test_average_without_grades(self):
        with self.assertRaises(ValueError):
            service.compute_average(self.data, self.sid, "CS101")


if __name__ == "__main__":
    unittest.main()
