from app.database.connection import get_connection


def add_expense(amount, category, description, date, currency):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO expenses
        (amount, category, description, date, currency)
        VALUES (?, ?, ?, ?, ?)
        """,
        (amount, category, description, date, currency)
    )

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return expense_id


def get_expenses():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, amount, category, description, date, currency
        FROM expenses
        ORDER BY date DESC
        """
    ).fetchall()

    connection.close()

    return rows



def get_expenses_by_category(category):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, amount, category, description, date, currency
        FROM expenses
        WHERE LOWER(category) = LOWER(?)
        ORDER BY date DESC
        """,
        (category,)
    ).fetchall()

    connection.close()

    return rows


def get_expenses_by_date_range(start_date, end_date):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, amount, category, description, date, currency
        FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
        """,
        (start_date, end_date)
    ).fetchall()

    connection.close()

    return rows



def get_total_expenses(category=None, start_date=None, end_date=None):
    connection = get_connection()

    query = "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    total = connection.execute(query, params).fetchone()[0]

    connection.close()

    return total