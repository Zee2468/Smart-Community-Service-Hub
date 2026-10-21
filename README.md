# eMangweni Smart Community Hub

A Django community portal for residents to report local service issues, track status updates, discover events and explore opportunities. Staff accounts have a separate administration workspace for managing reports and viewing live summaries.

## Requirements

- Python 3.12 or newer (Python versions supported by Django 5.2)
- pip
- Internet access in the browser for the Bootstrap, Bootstrap Icons and Chart.js CDN assets

## Run locally on Windows

Open Command Prompt in this project folder:

```cmd
py -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

**Existing database:** this project includes the database from the supplied project archive. Back up `db.sqlite3` and the `media` folder before replacing files or applying changes. Do not delete the database or migrations to troubleshoot a template issue.

## Accounts and permissions

- Residents register through the public registration page and can manage only their own reports.
- Staff accounts (`is_staff=True`) see the administration sidebar and can update the status of any report.
- To create a staff account locally, run `python manage.py createsuperuser`, or use Django admin to mark an existing trusted account as staff.
- Creating and editing shared events/opportunities is restricted to staff accounts.
- Signing out and marking notifications as read use POST forms with CSRF protection.

## Configuration

For local development, Django uses a development-only fallback secret key and `DEBUG=True`. Before deploying publicly, set environment variables for a strong secret key and production settings, for example:

```cmd
set DJANGO_SECRET_KEY=replace-with-a-long-random-secret
set DJANGO_DEBUG=false
set DJANGO_ALLOWED_HOSTS=your-domain.example
```

Configure HTTPS, secure cookies, email delivery and a production database before public deployment. The settings page in the admin portal is informational; it does not change deployment configuration.
