# Professional Billing System (FastAPI + Jinja)

## Requirements
- Python 3.10+

## Setup Instructions

1. Install dependencies:

pip install -r requirements.txt

2. Run application:

uvicorn app.main:app --reload

3. Open browser:

http://127.0.0.1:8000

---

## Features

- Product CRUD
- Billing generation
- Stock validation
- Tax calculation
- DB-driven denomination handling
- Change calculation algorithm
- Async email simulation
- Purchase history view

---

## Assumptions

- SQLite used for simplicity.
- Default denominations seeded on startup.
- Email sending simulated via console output.
- No authentication required.
- Basic HTML styling as per assignment instructions.