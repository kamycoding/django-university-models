from django.db import models


class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"


class StudentCard(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="card"
    )
    card_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.card_number


class Professor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Semester(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "year"], name="unique_semester_name_year"
            )
        ]

    def __str__(self):
        return f"{self.name} {self.year}"


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    professor = models.ForeignKey(
        Professor, on_delete=models.PROTECT, related_name="courses"
    )
    semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT, related_name="courses"
    )
    students = models.ManyToManyField(Student, related_name="courses", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "semester"], name="unique_course_code_semester"
            )
        ]

    def __str__(self):
        return f"{self.code}: {self.title} ({self.semester})"


class CourseDescription(models.Model):
    course = models.OneToOneField(
        Course, on_delete=models.CASCADE, related_name="description"
    )
    text = models.TextField()

    def __str__(self):
        return f"Description for {self.course}"
