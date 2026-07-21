# MenuWise

A Django REST Framework backend service that imports, validates, stores, and exposes supplier product pricing data.

The project demonstrates a production-oriented backend architecture with clean separation of concerns, efficient bulk imports, RESTful APIs, data validation, Django Admin integration, web scraping, and automated testing.

---

## Features

- Supplier and Product management
- CSV product import with validation
- Duplicate detection
- Bulk database inserts for efficient imports
- REST APIs with filtering, search, and pagination
- Django Admin support
- HTML supplier price scraping
- PostgreSQL database
- Automated tests using pytest

---

## Technology Stack

- Python 3.12+
- Django 6.x
- Django REST Framework
- PostgreSQL
- django-filter
- BeautifulSoup4
- Requests
- pytest
- pytest-django

---

## Project Structure

```
MenuWise/
│
├── apps/
│   ├── imports/
│   ├── products/
│   ├── scrapers/
│   └── suppliers/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── static/
├── manage.py
├── requirements.txt
├── pytest.ini
├── README.md
└── CONTRIBUTING.md
```

---

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd MenuWise
```

---

### Create Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Configure the following environment variables before running the application.

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| DATABASE_NAME | PostgreSQL database name |
| DATABASE_USER | PostgreSQL username |
| DATABASE_PASSWORD | PostgreSQL password |
| DATABASE_HOST | PostgreSQL host |
| DATABASE_PORT | PostgreSQL port |

Example:

```bash
export SECRET_KEY="your-secret-key"
export DATABASE_NAME="menuwisedb"
export DATABASE_USER="menuwise"
export DATABASE_PASSWORD="password"
export DATABASE_HOST="localhost"
export DATABASE_PORT="5432"
```

---

## Database Setup

Run migrations.

```bash
python manage.py migrate
```

Create a superuser.

```bash
python manage.py createsuperuser
```

Run the development server.

```bash
python manage.py runserver
```

---

## Running Tests

Execute all tests.

```bash
pytest
```

---

## REST API

### Suppliers

| Method | Endpoint |
|---------|----------|
| GET | `/api/v1/suppliers/` |

---

### Products

| Method | Endpoint |
|---------|----------|
| GET | `/api/v1/products/` |
| GET | `/api/v1/products/<id>/` |

Supported query parameters:

- supplier
- currency
- active_supplier
- search

Example:

```
GET /api/v1/products/?supplier=1
```

```
GET /api/v1/products/?currency=INR
```

```
GET /api/v1/products/?search=rice
```

---

### CSV Import

```
POST /api/v1/imports/products/
```

Multipart form-data

| Field | Description |
|------|-------------|
| file | CSV file |

---

## CSV Format

Expected columns:

| Column |
|----------|
| supplier_id |
| supplier_sku |
| product_name |
| pack_size |
| unit |
| currency |
| price |

---

## Data Validation

The application validates imported data before persistence.

Business rules include:

- Supplier SKU must be unique per supplier.
- Price cannot be negative.
- Pack size must be greater than zero.
- Units are normalized to:
  - g
  - kg
  - ml
  - l
  - each
- Missing currency defaults to:
  - INR for Indian suppliers
  - USD for all other suppliers

Invalid records are skipped while valid records continue to be imported.

---

## Django Admin

The project includes Django Admin configuration for:

- Supplier management
- Product management
- Search
- Filters
- Import visibility

---

## Web Scraping

A supplier price scraper is included using:

- Requests
- BeautifulSoup

The scraper:

- Parses supplier pricing data
- Normalizes units
- Validates records
- Stores products

---

## Design Decisions

Some implementation decisions made during development:

- PostgreSQL is used as the primary database.
- Bulk inserts are used for efficient CSV imports.
- Duplicate products are safely skipped.
- Business validation is centralized in the import service.
- Django REST Framework generic views are used for API endpoints.
- Filtering is implemented using django-filter.
- Tests are written using pytest and pytest-django.

---

## Future Improvements

Possible production enhancements include:

- Authentication and authorization
- OpenAPI / Swagger documentation
- Celery for asynchronous imports
- Structured logging
- Docker support
- CI/CD pipeline
- Import history and audit logging
- Object storage integration for uploaded files

---

## License

This project was developed as part of a backend engineering technical assessment.