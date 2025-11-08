# Flask-Blog

A small, starter Flask blog application written in Python and HTML. This repository contains the basics to run a simple blog locally and to extend it with features like user authentication, posting, and templates.

## Features
- Simple Flask app structure (Python + HTML templates)
- Basic routing and template rendering
- Ready to add persistence (SQLite / other DB)
- Easy to extend with authentication, forms, and API endpoints

## Requirements
- Python 3.8+
- pip

Optional (recommended)
- virtualenv or venv
- SQLite (built-in) or a different database
- python-dotenv for environment variables
- Flask-Migrate / Alembic for database migrations

## Quick start

1. Clone the repository
```bash
git clone https://github.com/CadeCustard/Flask-Blog.git
cd Flask-Blog
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
# On macOS / Linux
source .venv/bin/activate
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies
If a requirements.txt exists:
```bash
pip install -r requirements.txt
```
If using pyproject.toml / poetry, follow the corresponding install steps.

4. Configure environment variables
Create a .env file (or export vars) and set configuration values used by your app. Typical variables:
```
FLASK_APP=app.py           # or run.py / wsgi.py / your create_app entry
FLASK_ENV=development      # optional
SECRET_KEY=replace-with-secure-random-value
DATABASE_URL=sqlite:///app.db   # optional
```

5. Run the app
If the project uses the Flask CLI:
```bash
flask run
```
Or run the entrypoint directly:
```bash
python app.py
# or
python run.py
```
Visit http://127.0.0.1:5000 in your browser.
