# Engineering Decisions

This document captures the key architectural and implementation decisions made during the development of the MenuWise backend service.

---

# Project Objectives

The primary goals of this implementation were:

* Build a clean and maintainable Django REST Framework application.
* Follow a production-oriented project structure.
* Ensure data integrity through application and database-level validation.
* Efficiently import large CSV datasets.
* Expose RESTful APIs with filtering, searching, and pagination.
* Provide comprehensive automated tests.
* Keep the codebase modular and easy to extend.

---

# Architecture

The project follows a modular application structure where each business domain is implemented as an independent Django app.

```
apps/
├── suppliers/
├── products/
├── imports/
└── scrapers/
```

### Why?

* Clear separation of responsibilities.
* Easier maintenance and testing.
* Better scalability as new domains are introduced.
* Reduced coupling between business modules.

---

# Business Logic in Services

Complex business operations are implemented within dedicated service classes instead of API views.

Examples include:

* CSV import
* Data validation
* Data normalization
* Web scraping

### Why?

* Keeps API views lightweight.
* Improves code reuse.
* Makes business logic easier to test independently.
* Follows the Single Responsibility Principle.

---

# Database Constraints

Important validation rules are enforced at the database level wherever possible.

Examples include:

* Unique supplier SKU per supplier.
* Non-negative product price.
* Positive pack size.

### Why?

Database constraints provide an additional layer of protection against invalid data, even if records are inserted outside the application.

---

# Bulk CSV Import

Products are inserted using Django's `bulk_create()`.

### Why?

* Reduces the number of database queries.
* Improves performance for large imports.
* Supports importing thousands of records efficiently.

---

# Duplicate Handling

Duplicate products are identified using the combination of:

* Supplier
* Supplier SKU

Duplicate rows are skipped while continuing to process the remaining valid records.

### Why?

This approach prevents duplicate data while ensuring that one invalid record does not stop the entire import process.

---

# Unit Normalization

Supplier-provided units are normalized to a controlled set of values:

* g
* kg
* ml
* l
* each

### Why?

Suppliers often provide inconsistent unit representations. Normalization ensures consistent storage and simplifies downstream processing.

---

# Currency Defaults

If a currency is not provided during import:

* Suppliers from India default to **INR**
* All other suppliers default to **USD**

### Why?

This satisfies the business requirement while minimizing manual corrections for incomplete supplier data.

---

# REST API Design

The project uses Django REST Framework generic views together with `django-filter`.

Features include:

* Pagination
* Searching
* Filtering
* Detail endpoints

### Why?

DRF generic views provide a clean, maintainable implementation while minimizing boilerplate code.

---

# Testing Strategy

Automated tests cover:

* Model validation
* CSV import
* API endpoints
* Filtering
* Searching
* Duplicate handling

### Why?

The objective was to validate both business rules and API behavior while providing confidence during future code changes.

---

# Future Improvements

Potential production enhancements include:

* Authentication and authorization
* OpenAPI / Swagger documentation
* Asynchronous CSV imports (Celery)
* Structured logging
* Docker support
* CI/CD pipeline
* Import history and audit logging
* Object storage for uploaded files

---

# Use of AI Assistance

Artificial intelligence tools were used as a development aid during this project.

AI assistance was primarily used for:

* Drafting and refining project documentation (README, API documentation, contributing guide, and this document).
* Generating representative sample CSV files for testing and demonstration purposes.
* Discussing architectural approaches and reviewing portions of the implementation for readability and maintainability.
* Suggesting non-functional improvements and minor code optimizations.

All architectural decisions, implementation choices, validation logic, testing, integration, and final code review were performed by the project author. AI-generated suggestions were reviewed, adapted where appropriate, and verified through implementation and automated testing before inclusion in the project.
