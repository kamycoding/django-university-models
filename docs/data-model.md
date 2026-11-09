# University Database Model

## Overview

This project models a simple university database using Django ORM.

## Models and Relationships

| Model             | Relationship                            | Django Field    |
| ----------------- | --------------------------------------- | --------------- |
| Student           | Many-to-Many with Course                | ManyToManyField |
| StudentCard       | One-to-One with Student                 | OneToOneField   |
| Professor         | One-to-Many with Course                 | ForeignKey      |
| Course            | Many-to-One with Professor and Semester | ForeignKey      |
| CourseDescription | One-to-One with Course                  | OneToOneField   |
| Semester          | One-to-Many with Course                 | ForeignKey      |

## Architecture Decisions

### Course and Semester

Each Course represents a course offering in a specific semester.

### Professor and Course

Each Course has one Professor. A Professor can teach multiple Courses.

Deleting a Professor is restricted using PROTECT to prevent accidental deletion of associated Courses.

### Semester and Course

Each Course belongs to one Semester. A Semester can contain multiple Courses.

Deleting a Semester is restricted using PROTECT while Courses reference it.

### Student and Course

Students can enroll in multiple Courses, and each Course can have multiple Students.

### StudentCard and CourseDescription

Each Student has one StudentCard, and each Course has one CourseDescription.

Both relationships use OneToOneField.
