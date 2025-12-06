# APARTMENT UNIT ALLOCATOR

## Overview
The Apartment Unit Allocation CLI is a Python application designed for real estate developers to manage apartment unit assignments. It allows developers to register customers, add available units, and allocate units based on availability, preferences, and budget constraints.

## Key Features
- Register customers with budget and preferences
- Add apartment units with details (floor, type, price, status)
- Allocate units to customers fairly and efficiently
- Generate allocation reports directly from the CLI
- Built with SQLAlchemy ORM, Pipenv, and follows modular package structure

## Installation

1. Install dependencies:
```bash
pipenv install
```

2. Activate virtual environment:
```bash
pipenv shell
```

3. Install the package:
```bash
pip install -e .
```

## Usage

Run the interactive CLI:
```bash
apartment-allocator
```

The application provides interactive menus for:
- **Customer Management**: Create, view, find, and delete customers
- **Unit Management**: Create, view, find, allocate, and delete units
- **Relationship Management**: View customer's units and allocate units to customers

### Menu Navigation
- Main menu offers Customer Management and Unit Management
- Each submenu provides full CRUD operations
- Input validation with helpful error messages
- Type 'Ctrl+C' to exit at any time

## Database Schema
- **Customers**: id, name, budget, preferences
- **Units**: id, unit_number, floor, unit_type, price, status, customer_id
- **Relationship**: One Customer can have many Units (one-to-many)

## Project Structure
```
apartment_allocator/
├── apartment_allocator/
│   ├── __init__.py
│   ├── cli.py          # Interactive CLI with menus
│   ├── models.py       # SQLAlchemy ORM models with methods
│   └── database.py     # DB session setup
├── Pipfile
├── setup.py
└── README.md
```

## Features
- **Interactive Menus**: User-friendly CLI with numbered options
- **Input Validation**: Comprehensive error handling and validation
- **ORM Methods**: Each model includes create, delete, get_all, find_by_id
- **One-to-Many Relationship**: Customers can have multiple units