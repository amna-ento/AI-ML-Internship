from app.database.database import get_connection


def create_task(user_id: int, title: str):
    connection = get_connection()

    user = connection.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        raise ValueError("User not found")

    cursor = connection.execute(
        """
        INSERT INTO tasks (user_id, title)
        VALUES (?, ?)
        """,
        (user_id, title)
    )

    connection.commit()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    connection.close()

    return dict(task)


def list_tasks(user_id: int):
    connection = get_connection()

    user = connection.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        raise ValueError("User not found")

    tasks = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]