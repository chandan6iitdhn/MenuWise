# Contributing Guide

Thank you for your interest in contributing to MenuWise.

This document outlines the recommended development workflow, coding standards, and best practices for maintaining a clean, consistent, and production-ready codebase.

---

# Development Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
cd MenuWise
```

---

## 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Configure the following environment variables before running the application.

- SECRET_KEY
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT

---

## 5. Apply Migrations

```bash
python manage.py migrate
```

---

## 6. Run the Development Server

```bash
python manage.py runserver
```

---

# Development Workflow

1. Create a new branch from `main`.

```bash
git checkout -b feature/<feature-name>
```

Examples

```
feature/csv-import-validation
feature/product-filtering
bugfix/fix-currency-validation
```

---

2. Make small, focused commits.

Example commit messages:

```
Add product filtering by currency

Improve CSV validation

Handle duplicate supplier SKU

Refactor import service

Add scraper tests
```

---

3. Before opening a pull request, ensure:

- All tests pass
- No unnecessary files are committed
- Migrations are included if models changed
- Code is properly documented where required

---

# Coding Standards

## Python

- Follow PEP 8 guidelines.
- Use descriptive variable and function names.
- Keep functions focused on a single responsibility.
- Avoid deeply nested logic.
- Prefer readability over clever code.

---

## Django

### Models

- Keep business constraints close to the model.
- Use database constraints where appropriate.
- Add indexes for frequently queried fields.
- Use meaningful `related_name` values.

---

### Views

- Keep views thin.
- Delegate business logic to services.
- Avoid writing complex logic inside API views.

---

### Services

Business logic should live inside service classes whenever possible.

Examples:

- CSV import
- Data validation
- Data normalization
- Scraping
- Third-party integrations

---

### Serializers

Serializers should focus on:

- Validation
- Serialization
- Deserialization

Avoid placing business logic inside serializers.

---

# Database Changes

Whenever models change:

```bash
python manage.py makemigrations
python manage.py migrate
```

Review generated migrations before committing them.

---

# Testing

Run the complete test suite before submitting changes.

```bash
pytest
```

Tests should cover:

- Model validation
- API endpoints
- Import services
- Scrapers
- Duplicate handling
- Edge cases

---

# API Design Guidelines

- Follow REST principles.
- Return appropriate HTTP status codes.
- Validate all incoming data.
- Return meaningful error messages.
- Keep response formats consistent.

---

# Performance Guidelines

Prefer:

- `select_related()`
- `prefetch_related()`
- `bulk_create()`
- Database filtering over Python filtering

Avoid unnecessary database queries inside loops.

---

# Project Structure

New features should follow the existing application structure.

```
apps/

    suppliers/

    products/

    imports/

    scrapers/
```

Avoid creating utility modules that mix unrelated responsibilities.

---

# Pull Request Checklist

Before submitting a pull request, verify:

- [ ] Project builds successfully
- [ ] All tests pass
- [ ] No debugging code remains
- [ ] Migrations are included (if applicable)
- [ ] Documentation is updated
- [ ] New functionality includes tests
- [ ] Existing tests continue to pass

---

# Reporting Issues

When reporting an issue, include:

- Description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Relevant logs or screenshots (if applicable)

---

# Future Enhancements

Potential future improvements include:

- Authentication & Authorization
- OpenAPI / Swagger documentation
- Asynchronous imports
- Docker support
- CI/CD pipeline
- Structured logging
- Monitoring & metrics
- Import history and auditing

---

Thank you for helping improve MenuWise.