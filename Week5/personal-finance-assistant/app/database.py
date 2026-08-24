import sqlite3
from pathlib import Path
from datetime import date


DB_PATH = Path(__file__).parent.parent / "data" / "expenses.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL
            )
            """
        )

        count = connection.execute(
            "SELECT COUNT(*) FROM expenses"
        ).fetchone()[0]

        if count == 0:
            sample_expenses = [
                ("Food", 5000, "PKR", "Groceries and meals", str(date.today())),
                ("Transport", 3000, "PKR", "Fuel and rides", str(date.today())),
                ("Shopping", 8000, "PKR", "Clothes and accessories", str(date.today())),
                ("Bills", 4000, "PKR", "Internet and utilities", str(date.today())),
                ("Entertainment", 2500, "PKR", "Movies and subscriptions", str(date.today()))
            ]

            connection.executemany(
                """
                INSERT INTO expenses
                (category, amount, currency, description, expense_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                sample_expenses
            )

        connection.commit()


def get_expenses(category: str | None = None):
    with get_connection() as connection:
        if category:
            rows = connection.execute(
                """
                SELECT id, category, amount, currency, description, expense_date
                FROM expenses
                WHERE LOWER(category) = LOWER(?)
                ORDER BY expense_date DESC
                """,
                (category,)
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id, category, amount, currency, description, expense_date
                FROM expenses
                ORDER BY expense_date DESC
                """
            ).fetchall()

    return [
        {
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "currency": row[3],
            "description": row[4],
            "expense_date": row[5]
        }
        for row in rows
    ]


def get_expense_summary():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            """
        ).fetchall()

    return [
        {
            "category": row[0],
            "total": row[1]
        }
        for row in rows
    ]