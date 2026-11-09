from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from .models import (
    Course,
    CourseDescription,
    Professor,
    Semester,
    Student,
    StudentCard,
)


class StudentCardTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_number="S001",
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
        )

    def test_student_can_have_a_card(self):
        card = StudentCard.objects.create(student=self.student, card_number="C001")

        self.assertEqual(self.student.card, card)

    def test_student_cannot_have_two_cards(self):
        StudentCard.objects.create(student=self.student, card_number="C001")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StudentCard.objects.create(
                    student=self.student, card_number="C002"
                )

    def test_deleting_student_cascades_to_card(self):
        card = StudentCard.objects.create(student=self.student, card_number="C001")

        self.student.delete()

        self.assertFalse(StudentCard.objects.filter(pk=card.pk).exists())


class CourseRelationshipTests(TestCase):
    def setUp(self):
        self.professor = Professor.objects.create(
            first_name="Grace", last_name="Hopper", email="grace@example.com"
        )
        self.semester = Semester.objects.create(name="Fall", year=2026)

    def create_course(self, code, professor=None, semester=None):
        return Course.objects.create(
            code=code,
            title=f"Course {code}",
            professor=professor or self.professor,
            semester=semester or self.semester,
        )

    def test_professor_can_teach_multiple_courses(self):
        first = self.create_course("CS101")
        second = self.create_course("CS102")

        self.assertCountEqual(self.professor.courses.all(), [first, second])

    def test_course_has_exactly_one_professor(self):
        course = self.create_course("CS101")
        other = Professor.objects.create(
            first_name="Alan", last_name="Turing", email="alan@example.com"
        )
        course.professor = other
        course.save()

        self.assertEqual(course.professor, other)
        self.assertFalse(self.professor.courses.filter(pk=course.pk).exists())

    def test_deleting_professor_with_courses_is_protected(self):
        self.create_course("CS101")

        with self.assertRaises(ProtectedError):
            self.professor.delete()

    def test_semester_can_contain_multiple_courses(self):
        first = self.create_course("CS101")
        second = self.create_course("CS102")

        self.assertCountEqual(self.semester.courses.all(), [first, second])

    def test_deleting_semester_with_courses_is_protected(self):
        self.create_course("CS101")

        with self.assertRaises(ProtectedError):
            self.semester.delete()

    def test_student_can_enroll_in_multiple_courses(self):
        student = Student.objects.create(
            student_number="S001",
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
        )
        first = self.create_course("CS101")
        second = self.create_course("CS102")
        first.students.add(student)
        second.students.add(student)

        self.assertCountEqual(student.courses.all(), [first, second])

    def test_course_can_have_multiple_students(self):
        first = Student.objects.create(
            student_number="S001",
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
        )
        second = Student.objects.create(
            student_number="S002",
            first_name="Alan",
            last_name="Turing",
            email="alan@example.com",
        )
        course = self.create_course("CS101")
        course.students.add(first, second)

        self.assertCountEqual(course.students.all(), [first, second])

    def test_description_belongs_to_exactly_one_course(self):
        course = self.create_course("CS101")
        description = CourseDescription.objects.create(
            course=course, text="Introduction to computing"
        )

        self.assertEqual(course.description, description)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CourseDescription.objects.create(
                    course=course, text="Another description"
                )

    def test_deleting_course_cascades_to_description(self):
        course = self.create_course("CS101")
        description = CourseDescription.objects.create(
            course=course, text="Introduction to computing"
        )

        course.delete()

        self.assertFalse(
            CourseDescription.objects.filter(pk=description.pk).exists()
        )

    def test_duplicate_semester_name_and_year_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Semester.objects.create(name="Fall", year=2026)

    def test_duplicate_course_code_in_semester_is_rejected(self):
        self.create_course("CS101")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.create_course("CS101")
