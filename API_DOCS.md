# MenuWise API Documentation

## Base URL

```
/api/v1/
```

---

# Authentication

Currently, the APIs do not require authentication.

> **Note:** Authentication can be added in future using JWT, OAuth2, or Session Authentication.

---

# Common Response Codes

| Status Code | Description |
|------------|-------------|
| 200 | Request successful |
| 201 | Resource created successfully |
| 400 | Validation error |
| 404 | Resource not found |
| 500 | Internal server error |

---

# Pagination

Product listing supports pagination.

Example:

```
GET /api/v1/products/?page=2
```

Example Response

```json
{
    "count": 125,
    "next": "http://localhost:8000/api/v1/products/?page=3",
    "previous": "http://localhost:8000/api/v1/products/?page=1",
    "results": [
        {
            "id": 15,
            "supplier": 1,
            "supplier_sku": "SKU100",
            "product_name": "Basmati Rice",
            "pack_size": "5.00",
            "unit": "kg",
            "currency": "INR",
            "price": "420.00",
            "imported_at": "2026-07-20T18:45:12Z"
        }
    ]
}
```

---

# Suppliers

## Get All Suppliers

```
GET /api/v1/suppliers/
```

### Response

```json
[
    {
        "id": 1,
        "name": "ABC Foods",
        "country_code": "IN",
        "active": true,
        "created_at": "2026-07-20T15:30:10Z"
    },
    {
        "id": 2,
        "name": "Fresh Imports",
        "country_code": "US",
        "active": true,
        "created_at": "2026-07-20T15:45:18Z"
    }
]
```

---

# Products

## Get Products

```
GET /api/v1/products/
```

### Query Parameters

| Parameter | Type | Description |
|----------|------|-------------|
| supplier | Integer | Filter by supplier id |
| currency | String | Filter by currency |
| active_supplier | Boolean | Return products from active suppliers only |
| search | String | Search by product name |
| page | Integer | Pagination |

Example

```
GET /api/v1/products/?currency=INR&search=rice
```

### Response

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "supplier": 1,
            "supplier_sku": "SKU001",
            "product_name": "Basmati Rice",
            "pack_size": "5.00",
            "unit": "kg",
            "currency": "INR",
            "price": "450.00",
            "imported_at": "2026-07-20T18:10:25Z"
        },
        {
            "id": 5,
            "supplier": 2,
            "supplier_sku": "SKU009",
            "product_name": "Brown Rice",
            "pack_size": "2.00",
            "unit": "kg",
            "currency": "INR",
            "price": "275.00",
            "imported_at": "2026-07-20T18:12:42Z"
        }
    ]
}
```

---

## Get Product Details

```
GET /api/v1/products/{id}/
```

Example

```
GET /api/v1/products/10/
```

### Response

```json
{
    "id": 10,
    "supplier": 1,
    "supplier_sku": "SKU101",
    "product_name": "Olive Oil",
    "pack_size": "1.00",
    "unit": "l",
    "currency": "USD",
    "price": "14.50",
    "imported_at": "2026-07-20T18:50:01Z"
}
```

### Resource Not Found

```json
{
    "detail": "No Product matches the given query."
}
```

---

# Product CSV Import

## Import Products

```
POST /api/v1/imports/products/
```

### Request

Content-Type

```
multipart/form-data
```

### Form Data

| Field | Type | Required |
|------|------|----------|
| file | File | Yes |

### Expected CSV Format

```csv
supplier_id,supplier_sku,product_name,pack_size,unit,currency,price
1,SKU001,Basmati Rice,5,kg,INR,450
1,SKU002,Wheat Flour,10,kg,INR,520
2,SKU101,Olive Oil,1,l,USD,15
```

---

## Successful Response

```json
{
    "created": 3,
    "skipped": 0,
    "errors": []
}
```

---

## Partial Success

```json
{
    "created": 2,
    "skipped": 2,
    "errors": [
        {
            "row": 3,
            "error": "Price cannot be negative."
        },
        {
            "row": 4,
            "error": "Supplier SKU already exists."
        }
    ]
}
```

---

## Missing File

```json
{
    "file": [
        "This field is required."
    ]
}
```

---

# Validation Rules

The importer enforces the following business rules.

| Rule | Description |
|------|-------------|
| Supplier SKU | Must be unique per supplier |
| Price | Cannot be negative |
| Pack Size | Must be greater than zero |
| Units | Must be normalized to `g`, `kg`, `ml`, `l`, or `each` |
| Currency | Defaults to `INR` for Indian suppliers and `USD` otherwise |

---

# Notes

- Duplicate products are skipped.
- Invalid records do not stop the import process.
- Bulk inserts are used for efficient imports.
- Product listing supports filtering, searching, and pagination.