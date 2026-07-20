# Billing Management System

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.13+
- PostgreSQL
- Git
- Virtual Environment (recommended)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <project_folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 4. Install Required Packages

Install all the required dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root by referring to the `.env.example` file.

Example:

```dotenv
# Database connection
DATABASE_URL=database_url

# Email configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-character-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

> **Note:** Replace the email credentials with your own if required.

---

## Database Migration

After configuring the `.env` file, run the following command to create all database tables:

```bash
alembic upgrade head
```

This command will:

- Create the required database schema and tables.
- Execute all Alembic migrations.

---

## Seed Initial Data

Once the migration is completed, start the FastAPI application.

During application startup, the initial product data will be automatically seeded into the database (if it has not already been seeded).

---

## Run the FastAPI Application

Start the server using:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## UI Configuration

After starting the FastAPI server:

1. Copy the FastAPI base URL.

Example:

```
http://127.0.0.1:8000
```

2. Open the UI project.

3. Navigate to:

```
billing_page1.js
```

4. Update the `API_BASE` value:

```javascript
const API_BASE = "http://127.0.0.1:8000";
```

5. Save the file and run the UI application.

---

## Project Setup Summary

1. Clone the repository.
2. Create and activate the virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the `.env` file using `.env.example`.
5. Run the database migration:

```bash
alembic upgrade head
```

6. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

7. Copy the FastAPI URL.
8. Update the `API_BASE` in `billing_page1.js`.
9. Run the UI application.

---

## API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## Notes

- Ensure PostgreSQL is running before executing migrations.
- Verify the `DATABASE_URL` in the `.env` file points to the correct database.
- Product seed data is inserted automatically during application startup and will not be duplicated if it already exists.
- Update the SMTP credentials in the `.env` file if using a different email account.
