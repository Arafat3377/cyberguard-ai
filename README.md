# AI-Based Cybersecurity Monitoring and Threat Detection Platform

Academic Django prototype for a simplified SOC environment for SMEs. The project follows the supplied project specification: security-log monitoring, preprocessing, anomaly detection, threat classification, severity assessment, alerts, incident analysis, recommendations, dashboard, incident management, reports, and an intelligent assistant.

## Technology stack
- Python + Django
- MySQL (intended database; SQLite fallback for quick demo when `DB_NAME` is not set)
- Django ORM
- HTML/CSS/JavaScript + Bootstrap
- Pandas / NumPy / scikit-learn / joblib
- Isolation Forest for anomaly detection
- Random Forest for threat classification
- Rule-based severity/recommendation layer for the academic prototype

## Quick start (SQLite demo)
1. Create and activate a virtual environment.
2. `pip install -r requirements.txt`
3. `python datasets/generate_dataset.py`
4. `python ml_engine/train.py`
5. `python manage.py makemigrations core`
6. `python manage.py migrate`
7. `python manage.py seed_demo`
8. `python manage.py runserver`
9. Open http://127.0.0.1:8000/
10. Create a regular account from `/register/`, or log in as the demo administrator with `admin@example.com` / `Admin12345!`.

## MySQL
Create a database named `cybersecurity_db`, copy `.env.example` to `.env` and export the variables in your shell (or configure them in your deployment environment). Install MySQL Server and the `mysqlclient` dependency. Then run `python manage.py migrate`.

## Main pages
- `/` Security Dashboard
- `/devices/` Devices
- `/events/` Security Events and filters
- `/alerts/` Alerts
- `/reports/` Reports
- `/assistant/` AI Security Assistant
- `/admin/` Django administration

## User roles
- Staff users (`is_staff`) see the administrator dashboard and can update incident status. Django administration provides management for devices, events, alerts, and users; grant the required Django model permissions to staff accounts.
- Regular authenticated users see a separate read-only dashboard and can view monitoring data, reports, and recommendations. They cannot update incident status or access Django administration.
- Users can self-register at `/register/` with a unique email and password; new accounts are regular read-only users. Create or promote staff accounts and assign model permissions from `/admin/auth/user/` using a superuser account.

## ML workflow
The dataset is synthetic and safe. `datasets/generate_dataset.py` creates controlled normal and suspicious records. `ml_engine/train.py` trains the anomaly detector and classifier. The web platform currently uses stored event records for the dashboard and assistant; the ML pipeline is kept as a separate module so it can be integrated into ingestion as the next implementation step.

## Security notes
This is an educational defensive simulation. It does not launch attacks, scan third-party systems, or provide offensive tooling. Do not connect it to systems you do not own or have permission to monitor.

## Academic alignment
The report should describe this as a prototype/simplified SOC rather than a commercial SOC. For simulated data, use "near-real-time" or "simulated real-time" rather than claiming live production network monitoring.
