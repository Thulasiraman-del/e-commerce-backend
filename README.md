# E-Commerce Backend API

A RESTful e-commerce backend built with FastAPI, SQLAlchemy, PostgreSQL/SQLite support, Alembic, JWT authentication, and pytest.

## Features

- User registration and login
- JWT authentication
- Current user profile
- Product management
- Product categories
- Shopping cart management
- Address management
- Order creation and management
- Order status management
- Payment management
- Stock validation and reduction
- Database migrations with Alembic
- Automated API tests
- Docker support

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- JWT
- Pytest
- SQLite/PostgreSQL
- Docker

## Project Structure

```text
e-commerce-backend/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_addresses.py
│   ├── test_orders.py
│   ├── test_order_status.py
│   └── test_payments.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md