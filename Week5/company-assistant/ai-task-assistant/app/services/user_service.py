from app.database.database import get_connection


def get_user(user_id: int):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    if user is None:
        raise ValueError("User not found")

    return dict(user)


def create_user(name: str, email: str):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users (name, email)
        VALUES (?, ?)
        """,
        (name, email)
    )

    connection.commit()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()

    return dict(user)