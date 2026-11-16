# Fiscal Validator Web

> A lightweight Flask web interface for searching and consulting a structured knowledge base of validation issues.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-web%20app-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-data-3FCF8E?logo=supabase&logoColor=white)](https://supabase.com/)

## Overview

Fiscal Validator Web is a small Python/Flask application for viewing and searching records stored in Supabase. It provides a server-rendered interface and a searchable list of validation issues.

This is a **personal software project**, not an official product or service of any organization.

## Stack

- **Backend:** Python, Flask
- **Data:** Supabase
- **Templates:** HTML / Jinja
- **Production server:** Gunicorn
- **Deployment configuration:** Render

## Routes

| Route | Description |
| --- | --- |
| `/` | Landing page |
| `/criticas` | List validation records |
| `/criticas?busca=term` | Search records by supported fields |

## Run locally

```bash
git clone https://github.com/JoaoMalkiewiez/Validador-WEB.git
cd Validador-WEB
python -m venv .venv
```

Activate the virtual environment using your operating system's shell, then run:

```bash
pip install -r requirements.txt
python app.py
```

The application uses a Supabase project configured in `app.py`. Replace that configuration with **your own project and authorized data** before reuse. The database must provide a `criticas` table with the columns expected by the application.

## Deploy

The [`render.yaml`](render.yaml) file configures a Python web service using Gunicorn to serve the Flask `app` object. A successful deployment also depends on database availability, valid permissions and the expected schema.

## Security and limitations

- The current source contains a Supabase **publishable** key. Publishable keys are not service-role secrets, but database access still depends on correctly configured Row Level Security policies.
- Do not put service-role keys, customer data or confidential operational records in this repository.
- Review the query filter and error handling before exposing the service to untrusted traffic.
- This repository does not currently demonstrate an automated test suite.

## Author

**João Vitor Soares Malkiewiez** · [GitHub](https://github.com/JoaoMalkiewiez)
