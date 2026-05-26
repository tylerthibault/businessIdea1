# QuoteKit

> Quote and estimate builder for freelancers and contractors.

**Features:**
- Create and manage clients
- Build quotes with line items
- Shareable public link — clients can accept or decline
- PDF export
- Simple dashboard with revenue stats

## Quick Start

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit SECRET_KEY
flask db init && flask db migrate -m "init" && flask db upgrade
flask run
```

Open http://localhost:5000 — register, start building quotes.

## Deploy

One-click deploy to Railway or Render:
1. Set `DATABASE_URL` to a Postgres URL
2. Set `FLASK_ENV=production` and `SECRET_KEY`
3. Add start command: `flask db upgrade && gunicorn run:app`

---
Built with Flask · Bootstrap 5 · SQLAlchemy
