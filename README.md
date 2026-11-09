# 🎓 Django University Models

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1.3-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

A university database modeling project built with Django ORM. It demonstrates how students, professors, courses, semesters, and related records can be connected using relational database relationships.

The project focuses on data modeling, database integrity, migrations, and automated testing.

## ✨ Features

- **Relational database modeling** — six Django models representing a university system
- **One-to-one relationships** — student cards and course descriptions
- **One-to-many relationships** — professors and semesters linked to courses
- **Many-to-many relationships** — students enrolled in multiple courses
- **Data integrity** — unique constraints and controlled deletion behavior
- **Database migrations** — schema generation and management using Django ORM
- **Automated testing** — 14 tests covering relationships, constraints, and deletion behavior

## 🛠 Tech Stack

| Component       | Technology      |
| --------------- | --------------- |
| Language        | Python          |
| Framework       | Django 6.1.3    |
| Database        | SQLite          |
| ORM             | Django ORM      |
| Testing         | Django TestCase |
| Version Control | Git & GitHub    |

## 📁 Project Structure

```text
django-university-models/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── university/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── docs/
│   └── data-model.md
├── .env.example
├── .gitignore
├── manage.py
└── README.md
```

## 🗃 Database Models

The database contains six models.

| Model               | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `Student`           | Stores student information and enrollment relationships       |
| `StudentCard`       | Stores a unique identification card associated with a student |
| `Professor`         | Stores professor information                                  |
| `Course`            | Represents a course offered in a specific semester            |
| `CourseDescription` | Stores the description associated with a course               |
| `Semester`          | Organizes courses by academic semester                        |

## 🔗 Database Relationships

| Relationship               | Type               | Django Field      |
| -------------------------- | ------------------ | ----------------- |
| Student → StudentCard      | One-to-One (1:1)   | `OneToOneField`   |
| Professor → Course         | One-to-Many (1:N)  | `ForeignKey`      |
| Student ↔ Course           | Many-to-Many (M:N) | `ManyToManyField` |
| Course → CourseDescription | One-to-One (1:1)   | `OneToOneField`   |
| Semester → Course          | One-to-Many (1:N)  | `ForeignKey`      |

### One-to-One

Each student can have one student card, and each course can have one course description.

Django's `OneToOneField` ensures that no student or course is associated with more than one corresponding record. The related records are not automatically created.

### One-to-Many

A professor can teach multiple courses, but each course references exactly one professor.

Similarly, a semester can contain multiple courses, while each course belongs to one semester.

These relationships use `ForeignKey` fields on the `Course` model.

### Many-to-Many

A student can attend multiple courses, and each course can have multiple students.

Django manages this relationship through `ManyToManyField` and an intermediate database table.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kamycoding/django-university-models.git
cd django-university-models
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Django

```bash
python -m pip install Django==6.1.3
```

### 4. Configure the environment

The project reads its Django secret key from the `DJANGO_SECRET_KEY` environment variable.

Generate a local development key:

```bash
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
```

The included `.env.example` documents the required environment variable.

Django does not automatically load `.env` files. The key must be provided through the environment before running management commands.

### 5. Apply database migrations

```bash
python manage.py migrate
```

This creates the SQLite database and applies the university models alongside Django's built-in migrations.

### 6. Run the Django development server

```bash
python manage.py runserver
```

The development server starts at:

**http://127.0.0.1:8000/**

This project focuses on database modeling. It does not provide a custom frontend or REST API.

## 🧩 Database Schema

Django defines the database structure through the models in `university/models.py`.

The initial migration is stored in:

`university/migrations/0001_initial.py`

To generate migrations after changing a model:

```bash
python manage.py makemigrations
```

To apply pending migrations:

```bash
python manage.py migrate
```

To check for model changes that have not been captured in migrations:

```bash
python manage.py makemigrations --check --dry-run
```

## 🏗 Architecture Decisions

### Course and Semester

Each `Course` represents a course offering in one specific semester.

The same course code may appear in different semesters, but duplicate course codes within the same semester are prevented by a database constraint.

### Deletion Behavior

The project uses two Django deletion strategies:

| Relationship               | Behavior  |
| -------------------------- | --------- |
| Student → StudentCard      | `CASCADE` |
| Course → CourseDescription | `CASCADE` |
| Professor → Course         | `PROTECT` |
| Semester → Course          | `PROTECT` |

`CASCADE` removes dependent records when their parent record is deleted.

`PROTECT` prevents deleting a professor or semester while courses still reference them.

### Unique Constraints

- Student numbers are unique.
- Student and professor email addresses are unique within their respective models.
- Student card numbers are unique.
- Semester name and year combinations are unique.
- Course codes are unique within each semester.

These constraints help maintain consistent data and prevent duplicate records.

Further details are available in [docs/data-model.md](docs/data-model.md).

## ✅ Testing & Verification

The project includes 14 automated tests covering model relationships, uniqueness constraints, and deletion behavior.

Run all university model tests:

```bash
python manage.py test university
```

Run Django's system checks:

```bash
python manage.py check
```

Verify the migration state:

```bash
python manage.py makemigrations --check --dry-run
```

**Last reported validation:**

- Django system checks passed.
- All database migrations applied successfully.
- No pending model changes detected.
- 14 tests passed.

Run these commands from the project root with the virtual environment active and `DJANGO_SECRET_KEY` configured.
