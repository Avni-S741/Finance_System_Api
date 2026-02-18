📌 EXPENSE TRACKER API

A backend expense management system built with FastAPI and SQLite, designed to demonstrate clean API structure, input validation, soft delete logic, and data normalization.

🚀 FEATURES

Create, update, delete (soft delete) expenses

Restore deleted expenses

Get all active expenses

Get expense by ID

Category-wise spending summary

Input validation using Pydantic

ISO date enforcement (YYYY-MM-DD)

Data normalization (consistent category handling)

Response models for strict API contracts

🛠 TECH STACK

Python

FastAPI

SQLite

Pydantic


🧠 DESIGN DECISIONS

Soft Delete instead of hard delete to preserve historical data.

Normalization layer to prevent inconsistent category entries.

Response models used to enforce strict API output structure.

Date stored in ISO format to maintain proper sorting and compatibility.

📌 FUTURE IMPROVEMENTS

Authentication & authorization

Pagination support

Async DB support

📖 LEARNING PURPOSE

This project was built to strengthen backend fundamentals including:

API design

Data validation

Business logic separation

Schema enforcement

Handling schema evolution issues