# Universitätsdatenbank mit Django

## Projektüberblick

Dieses Kursprojekt bildet eine einfache Universitätsdatenbank mit dem Django ORM ab. Im Mittelpunkt stehen Modellfelder, Beziehungen, Löschregeln und Datenbank-Constraints. Die Anwendung verwendet SQLite und enthält Tests für die wichtigsten Regeln.

## Datenmodelle und Beziehungen

| Modell | Aufgabe und Beziehung |
| --- | --- |
| `Student` | Studierende mit eindeutiger Matrikelnummer und E-Mail-Adresse; können mehrere Kurse belegen. |
| `StudentCard` | Karte mit eindeutiger Kartennummer; über `OneToOneField` höchstens eine pro Student. |
| `Professor` | Lehrperson mit eindeutiger E-Mail-Adresse; kann mehrere Kurse unterrichten. |
| `Course` | Kursangebot mit Code und Titel; gehört über je ein `ForeignKey` zu einem Professor und einem Semester. |
| `CourseDescription` | Beschreibungstext; über `OneToOneField` höchstens eine pro Kurs. |
| `Semester` | Semester mit Name und Jahr; kann mehrere Kurse enthalten. |

Zwischen `Course` und `Student` besteht ein `ManyToManyField`: Ein Kurs kann mehrere Studierende haben, und Studierende können mehrere Kurse belegen. Die vollständige Beziehungsskizze steht in [docs/data-model.md](docs/data-model.md).

## Technischer Aufbau

Die Modelle liegen in `university/models.py`, die Tests in `university/tests.py` und die initiale Migration in `university/migrations/0001_initial.py`. `config/settings.py` registriert die App `university`, verwendet SQLite und liest `DJANGO_SECRET_KEY` aus der Umgebung. Eine Abhängigkeitsdatei ist derzeit nicht vorhanden.

## Lokale Einrichtung

Unter Ubuntu/Linux im Projektverzeichnis:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install 'Django==6.1.3'
export DJANGO_SECRET_KEY="$(.venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
.venv/bin/python manage.py check
```

Die Datei `.env.example` zeigt nur den Namen der benötigten Umgebungsvariable und einen Platzhalter. Django lädt `.env`-Dateien nicht automatisch. Der obige `export` setzt einen temporären Entwicklungsschlüssel für die aktuelle Shell; der erzeugte Wert wird nicht im Repository gespeichert. Bei einer neuen Shell muss die Variable erneut gesetzt werden.

## Datenbankmigrationen

Die initiale Migration für die sechs Modelle ist bereits vorhanden. Nach der lokalen Einrichtung wird sie so auf die SQLite-Datenbank angewendet:

```bash
.venv/bin/python manage.py migrate
```

## Tests

```bash
.venv/bin/python manage.py test university
```

Die Tests prüfen Beziehungen, Löschverhalten und Eindeutigkeitsregeln. Django erstellt dafür eine eigene Testdatenbank.

## Architekturentscheidungen

Ein `Course` ist ein Kursangebot in genau einem Semester. `UniqueConstraint` verhindert doppelte Semester aus Name und Jahr sowie doppelte Kurscodes innerhalb desselben Semesters; derselbe Code darf in einem anderen Semester erneut vorkommen. `CASCADE` entfernt eine `StudentCard` beim Löschen ihres Studenten und eine `CourseDescription` beim Löschen ihres Kurses. `PROTECT` verhindert das Löschen eines Professors oder Semesters, solange Kurse darauf verweisen.
