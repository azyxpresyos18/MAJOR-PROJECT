# Demo-District – Django Setup Guide
**DemoPower's Client-Product Departmentalization System**

---

## Quick Start (SQLite – Development)

```bash
# 1. Install dependencies
pip install django psycopg2-binary pillow

# 2. Run migrations
python manage.py migrate

# 3. Seed sample data + create admin user
python manage.py seed_data

# 4. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000
Login: **admin** / **admin123**

---

## Switch to PostgreSQL (Production)

### Step 1 – Create the database
```bash
psql -U postgres
CREATE DATABASE demodistrict;
CREATE USER demouser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE demodistrict TO demouser;
\q
```

### Step 2 – Update settings.py
In `demodistrict/settings.py`, comment out the SQLite block and uncomment:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'demodistrict',
        'USER': 'demouser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Step 3 – Migrate & seed
```bash
python manage.py migrate
python manage.py seed_data
```

---

## Project Structure

```
demodistrict/          ← Django config (settings, urls)
core/
  models.py            ← Client, Department, Product, Location, Schedule
  views.py             ← All page logic
  urls.py              ← URL routes
  admin.py             ← Admin panel config
  templates/core/      ← All HTML pages
  management/commands/ ← seed_data command
static/
  css/style.css        ← All styles
  js/main.js           ← JS utilities
  images/              ← Put your product images here
```

---

## Pages

| URL | Page |
|-----|------|
| `/` | Login |
| `/home/` | Dashboard |
| `/clients/` | Client list |
| `/products/` | Product grid (filterable by client) |
| `/departmentalize/` | Schedule table with status filter |
| `/location/` | Location/venue cards |
| `/schedule/` | Create & manage schedules |
| `/admin/` | Django admin panel |

---

## Adding Real Data

Use the Django Admin panel at `/admin/` to add:
- Clients (Coca-Cola, Nivea, etc.)
- Products (link to client + upload image)
- Departments (Sales, Marketing, etc.)
- Locations (malls, with availability)
- Schedules

Or use the seed command to reload sample data:
```bash
python manage.py seed_data
```

---

## Adding Product Images

1. Put image files in `static/images/`
2. Run `python manage.py collectstatic`
3. In the admin panel, upload images for each Product/Client

---

## API Endpoints (used by the frontend)

```
POST /api/schedule/<id>/status/   ← Update schedule status
POST /api/schedule/<id>/delete/   ← Delete a schedule
```

Both require CSRF token in header: `X-CSRFToken: <token>`
