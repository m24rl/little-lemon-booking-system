# Little Lemon booking system

Meta **The Full Stack** final project: Django project `littlelemon`, app `restaurant`, MySQL storage, and a JavaScript booking interface using `fetch`.

## Run with MySQL

Requires Python 3.11+ and a running MySQL server. Install Pipenv with `python -m pip install pipenv`.

1. Create an empty MySQL database: `CREATE DATABASE reservations CHARACTER SET utf8mb4;`.
2. Set `MYSQL_DATABASE`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, and `MYSQL_PASSWORD` in your shell as needed. Defaults are reservations, 127.0.0.1, 3306, root and an empty password. No personal credentials are included. Set `DJANGO_SECRET_KEY` to a persistent private value for any shared deployment.
3. From the directory containing manage.py:

```console
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

On PowerShell, set values with `$env:MYSQL_PASSWORD='your-local-password'`; on Bash use `export MYSQL_PASSWORD='your-local-password'`.

Open http://127.0.0.1:8000/book/ and http://127.0.0.1:8000/reservations/.

## Features and reviewer checks

- Three booking fields: first name, reservation date with native calendar picker, reservation slot (11 AM through 7 PM).
- Current local date is selected automatically and reservations load immediately.
- Changing the date fetches fresh availability. An empty date displays **No bookings**.
- Occupied slots are disabled. The backend and database constraint also prevent duplicate date/time reservations.
- `GET /bookings?date=2030-01-01` returns that date's reservations in JSON. `GET /bookings` returns all reservations.
- `POST /bookings` accepts a JSON object with first_name, reservation_date and reservation_slot; the same-origin form supplies its CSRF token. Success returns 201; malformed or invalid data returns 400; a concurrent booking conflict returns 409. Model-level duplicate validation can return 400 before the database insert.
- `/reservations/` displays all reservations as formatted JSON, safely embedded with Django's json_script filter.

Try reserving a date and time, then selecting that date again. The slot should be disabled. Try an unused date to see the empty state. The same slot on another date remains available.

## Verification

```console
pipenv run python manage.py check
pipenv run python manage.py test restaurant
```

Four automated workflow tests cover filtering and empty dates, duplicate prevention, invalid requests and JSON/form rendering. Local automated verification was performed with Django 5.2 and SQLite because a MySQL service was unavailable in the execution environment. MySQL remains the default backend and must be configured on the reviewer's machine; the SQLite test result does not establish MySQL connectivity.

For an optional local preview without MySQL, set `DJANGO_USE_SQLITE=1` before migration and startup. Unset it for the required MySQL setup. The repository excludes local databases, virtual environments and credentials. This is a development/coursework application, with DEBUG enabled; it is not configured as a public production service.
