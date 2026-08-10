# Habit Tracker (Flask)
live : https://habit-tracker-y5ic.onrender.com

A fullstack Flask app for tracking daily/weekly habits, streaks, and check-ins.

## Features
- User registration & login (Flask-Login, hashed passwords)
- Create/view/delete habits
- Daily check-ins with automatic streak calculation
- 30-day check-in heatmap on the habit detail page
- Flash messages, form validation (Flask-WTF)

## Setup (VS Code / local)

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   The `.env` file is already included with defaults. Change `SECRET_KEY` before deploying anywhere real.

4. **Run the app**
   ```bash
   python run.py
   ```
   The app will create `habits.db` (SQLite) automatically on first run and be available at `http://127.0.0.1:5000`.

5. **(Optional) Use Flask-Migrate instead of `db.create_all()`**
   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
   Note: `app/__init__.py` currently calls `db.create_all()` automatically, which is fine for development. For a "real" project, switch to migrations only, and remove the `db.create_all()` call.

## Project Structure
```
habit-tracker/
├── app/
│   ├── __init__.py       # App factory
│   ├── models.py         # User, Habit, HabitLog models
│   ├── forms.py          # WTForms
│   ├── routes/
│   │   ├── auth.py       # register/login/logout
│   │   └── habits.py     # habit CRUD + check-in
│   ├── templates/
│   └── static/
├── config.py
├── run.py
└── requirements.txt
```

## Deploying to Render

This project includes a `render.yaml` (Render "Blueprint") that sets up both the web service and a free PostgreSQL database automatically.

### Option A: One-click Blueprint deploy (recommended)
1. Push this project to a GitHub repo.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your repo. Render will read `render.yaml` and provision:
   - A free PostgreSQL database (`habit-tracker-db`)
   - A web service (`habit-tracker`) with a random `SECRET_KEY` auto-generated and `DATABASE_URL` wired to the database
4. Click **Apply** — Render will run `pip install -r requirements.txt && flask db upgrade` on build, then start the app with `gunicorn run:app`.
5. Once deployed, visit the `.onrender.com` URL Render gives you.

### Option B: Manual setup
1. Push to GitHub.
2. On Render: **New** → **PostgreSQL** → create a free database, copy its **Internal Database URL**.
3. **New** → **Web Service** → connect your repo.
   - **Build Command:** `pip install -r requirements.txt && flask db upgrade`
   - **Start Command:** `gunicorn run:app`
   - **Environment variables:**
     - `SECRET_KEY` — any long random string
     - `DATABASE_URL` — the Internal Database URL from step 2
     - `FLASK_APP` — `run.py`
4. Deploy.

### Notes
- The free Render Postgres tier expires after 90 days unless upgraded — fine for a demo/portfolio project, but keep that in mind.
- Do **not** rely on SQLite in production on Render — its filesystem is ephemeral, so your `habits.db` file (and all data) would be wiped on every redeploy/restart. That's why `render.yaml` provisions a real Postgres database instead.
- Migrations run automatically on every deploy via the build command. If you change models locally, run `flask db migrate -m "description"` and commit the new file in `migrations/versions/` before pushing.

## Next steps / ideas to extend
- Weekly habit logic (currently `frequency` is stored but streak logic assumes daily)
- Edit habit (currently only create/delete)
- Reminder emails (Flask-Mail)
- Charts with Chart.js instead of the CSS grid heatmap
- Deploy to Render/Railway/PythonAnywhere
